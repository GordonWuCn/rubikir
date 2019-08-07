#

# pylint: disable = unused-wildcard-import
from rubikir import *


# create a program instance, which uses queue APIs 
# include Insert, Assemble, External with queue=True, and Eject maybe in the future
ip_program = Program(queue_api=True)

# name declarations
# variable is per-packet temporary storage
identifier = ip_program.variable('identifier')
get_all = ip_program.variable('get_all')
# key is per-stream permanent storage
count = ip_program.key('count')
# state constants
START, MORE, DONE = 0, 1, 2

ip_program.set_code([
    # identifier = hash([packet.srcip, packet.dstip])
    Assign(identifier, Op('hash', [Field('srcip'), Field('dstip')])),
    # if identifier not in <instance table>:
    #     create instance at <instance table>[identifier]
    #     set <instance table>[identifier].count to 0
    Perpare(identifier, {count: Constant(0)}),
    # insert payload into instance's queue, at offset with length
    Insert(Field('offset'), Field('length'), Field('payload')),
    # get_all = <there's no hole in queue> && !packet.more_frag
    Assign(get_all, Op('and', [NoHole(), Op('not', [Field('more_frag')])])),
    # the only thing could be matched is state
    # which should always exist in instance permanent data
    Match({
        # case state == :start
        START: [
            # if packet.dont_frag:
            #     state = :done
            # else:
            #     state = :more
            # Notice that we pass common integer (START = 0, MORE = 1, DONE = 2) as 
            # SetState's argument rather than Constant(...)
            # it's meaningless to SetState(Constant('hello!'))
            IfElse(Field('dont_frag'), [
                SetState(DONE),
            ], [
                SetState(MORE),
            ]),
        ],
        MORE: [
            # if get_all: ...
            IfElse(Rval(get_all), [
                SetState(DONE),
            ], [
                SetState(MORE),
            ]),
        ],
    }),
    # perm.count = perm.count + 1
    Store(count, Op('add', [Load(count), Constant(1)])),
    Match({
        MORE: [
            # user_callback_1(packet.field1, packet.field2, perm.count)
            # the exact external cause (user_callback_1 here) will be added in the future
            External([Field('field1'), Field('field2'), Load(count)]),
        ],
        DONE: [
            # assemble payloads in the queue
            Assemble(),
            # user_callback_2(packet.field1, <queue>)
            External([Field('field1')], queue=True),
            External([Field('field1'), Field('field2'), Load(count)]),
            # tcp_protocol(packet.srcip, packet.dstip, <queue>)
            External([Field('srcip'), Field('dstip')], queue=True),
            # delete instance's permanent data from instance table
            Delete(),
        ]
    })
])
