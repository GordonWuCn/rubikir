#

# pylint: disable = unused-wildcard-import
from rubikir import *


# create a program instance, which uses queue APIs 
# include Insert, Assemble, External with queue=True, and Eject maybe in the future
ip_program = Program(name = 'ip', queue_api=True)

# name declarations
# variable is per-packet temporary storage
identifier = ip_program.variable('identifier')
# key is per-stream permanent storage
count = ip_program.key('count')
state = ip_program.key('state')
# state constants
START, MORE = 0, 1

finalize = [
    Assemble(),
    External([Field('srcip'), Field('dstip')], data=True),
    Delete(),
]

wait_for_more = [
    Assign(state, Constant(MORE))
]

ip_program.set_code([
    # identifier = hash([packet.srcip, packet.dstip])
    Assign(identifier, Op('hash', [Field('srcip'), Field('dstip')])),
    # if identifier not in <instance table>:
    #     create instance at <instance table>[identifier]
    #     set <instance table>[identifier].count to 0
    IfElse(Contain(identifier), [], [
        Create((identifier), {count: Constant(0), state: Constant(START)}),
    ]),
    Assign(count, Op('add', [count, Constant(1)])),
    # insert payload into instance's queue, at offset with length
    InsertMeta(Field('offset'), Field('length')),
    InsertData(Field('payload')),
    IfElse(Op('equal', [state, Constant(START)]), [
        IfElse(SeqSeen('dont_frag'), finalize, wait_for_more)
    ], [  # MORE
        IfElse(Field('more_frag'), wait_for_more, finalize),
    ])
])

print(ip_program)
