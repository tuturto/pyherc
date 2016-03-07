Finite-state machines
=====================

Finite-state machine is often used for artificial intelligence routines in
games. They can model different states character can be: patrolling, searching
for food, investigating noise and fighting. There is a small DSL for defining
finite-state machines supplied with pyherc.

Sample configuration
--------------------

Following code is a sample definition for a very simple finite-state machine.
It has two states ``addition`` and ``subtraction``.

.. code-block:: hy

   (defstatemachine SimpleAdder [message]
     "finite-state machine for demonstration purposes"

     "add 1 to message, 0 to switch state"
     (addition initial-state
               (active (+ message 1))

               "message 0 will change state"
               (transitions [(= message 0) subtraction]))

     "substract 1 from message, 0 to switch state"
     (subtraction (active (- message 1))

                  "message 0 will change state"
                  (transitions [(= message 0) addition])))

In order to use the finite-state machine, one needs to create an instance of
it and call it like a function:

.. code-block:: hy

   => (setv fsm (SimpleAdder))
   => (fsm 1)
   2
   => (fsm 2)
   3
   => (fsm 0)
   -1
   => (fsm 1)
   0
   => (fsm 2)
   1

As you can see, ``fsm`` will first return the argument passed to it plus 1.
As soon as ``0`` is passed in, finite-state machine switches to subtraction
state and starts returning the argument passed to it minus 1. Passing a ``0``
again will change the state back to addition.

Sometimes there's need to perform extra initialisation when finite-state
machine is created or store data across different states. Following example
highlights how ``--init--`` and ``state`` forms can be used to achieve this.

.. code-block:: hy

   (defstatemachine Minimal [message]
     "default initializer"
     (--init-- [bonus] (state bonus bonus))
     "handle message"
     (process initial-state
              (active (* message (state bonus)))))

Following example shows how the finite-state machine defined in previous
example can be used:

.. code-block:: hy

   => (setv fsm (Minimal 3))
   => (fsm 1)
   3
   => (fsm 5)
   15

As you can see, the parameter supplied during initialization of finite-state
machine is stored under symbol ``bonus`` and used when finite-state
machine is activated.

Syntax of finite-state machine definition
-----------------------------------------

Finite-state machine is defined with ``(defstatemachine <name> <parameters>)``
form. ``<name>`` defines name of the class that will encapsulate finite-state
machine definition. ``<parameters>`` is a list of zero or more symbols that
define function interface that the finite-state machine will have. Keyword
only, optional or other special parameter types are not supported.

Inside of ``defstatemachine`` form, there are one or more state definitions.
Strings are allowed and they're treated as comments (ie. ignored). Format
of state definition is
``(<name> [initial-state] [(on-activate ...)] [(active ...)] [(on-deactivate ...)] [(transitions ...)])``.
``<name>`` is name of the state, it should be unique within a finite-state
machine as transitions refer to them. One and only one of the states should be
marked as an ``initial-state``. This is the state the finite-state machine
will enter when first activated. Rest three forms are all optional. Order of
the forms is not significant. Symbols defined in ``<parameters>`` block of
``defstatemachine`` are available to all of these three functions. Strings
are allowed and they are treated as comments (ie. ignored). Special form
``--init--`` can be used to create initializer method for finite-state
machine. It has syntax of
``(--init-- <parameters> <body>)``. ``<parameters>`` is a list of symbols that
are to be added in ``--init--`` method of the finite-state machine and
``<body>`` is one or more s-expressions that are to be executed when
finite-state machine is initialized. 

First one is ``on-activate``, which defines code that is executed when the
given state is activated. Second one is ``active`` which defines code that is
executed every time for the active state when finite-state machine is
activated. ``on-activate`` is mirrored by ``on-deactivate``, which gets
executed every time a state deactivates.
The last one is ``transitions``. It defines one or more two element
lists, where the first element is test and second element is symbol of a
state to switch if the test returns true. ``transitions`` are checked for
the active state every time finite-state machine is activated and it is
performed before ``active`` code is executed.

In order to store data and pass it between states, ``state`` macro can be
used. It has syntax of: ``(state <symbol> [value])``. ``<symbol>`` is the
stored data being accessed. If optional ``value`` is supplied, stored data
is updated. In any case ``state`` returns the current value of the data.
