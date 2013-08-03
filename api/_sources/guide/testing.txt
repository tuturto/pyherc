Testing
*******
This section will have a look at various testing approaches utilised in the
writing of the game and how to add more tests.

Overview of testing
===================
Tools currently in use are:

 * nose_
 * doctest_
 * behave_
 * mockito-python_
 * pyhamcrest_

Nosetests are mainly used to help the design and development of the software.
They form nice safety net that catches bugs that might otherwise go unnoticed
for periods of time.

Doctest is used to ensure that code examples and snippets in documentation are
up to date.

Behave is used to write tests that are as close as possible to natural
language.

Additional tool called nosy_ can be used to run nosetests automatically as 
soon as any file change is detected. This is very useful when doing test
driven development.

Running tests
=============

Nose
----
Nose tests can be run by issuing following command in pyherc directory::

  nosetests
  
It should output series of dots as tests are executed and summary in
the end::

  ......................................................................
  ......................................................................
  ........................................
  ----------------------------------------------------------------------
  Ran 180 tests in 3.992s

If there are any problems with the tests (or the code they are testing),
error will be shown along with stack trace.
  
Doctest
-------
Running doctest is as simple. Navigate to the directory containing make.bat
for documentation containing tests (doc/api/) and issue command::

  make doctest
  
This will start sphinx and run the test. Results from each document are
displayed separately and finally summary will be shown::

  Doctest summary
  ===============
      4 tests
      0 failures in tests
      0 failures in setup code
      0 failuers in cleanup code
  build succeeded.
  
  Testing of doctests in the sources finished, look at the results in build/doctest/output.txt.
  
Results are also saved into a file that is placed to build/doctest/ directory

There is handy shortcut in main directory that will execute both and also
gather test coverage metrics from nosetests::

  suite.py

Coverage report is placed in cover - directory.

Behave
------
Navigate to directory containing tests written with behave (behave) and issue
command::

  behave
  
This will start behave and run all tests. Results for each feature are 
displayed on screen and finally a summary is shown::
      
    2 features passed, 0 failed, 0 skipped
    3 scenarios passed, 0 failed, 0 skipped
    21 steps passed, 0 failed, 0 skipped, 0 undefined
    Took 0m0.0s

Writing tests
=============

Unit tests
----------
Unit tests are placed in package :py:mod:`pyherc.test.unit` Any module that is
named as "test_*" will be inspected automatically by Nose when it is gathering
tests to run. It will search for classes named "Test*" and methods named 
"test_*".

Following code is simple test that creates EffectHandle object and tries to
add it into EffectsCollection object. Then it verifies that it actually was
added there.

.. testcode::

    from pyherc.data.effects import EffectsCollection
    from pyherc.test.builders import EffectHandleBuilder
    from hamcrest import *
    from pyherc.test.matchers import has_effect_handle

    class TestEffectsCollection(object):
    
        def __init__(self):
            super(TestEffectsCollection, self).__init__()
            self.collection = None
    
        def setup(self):
            """
            Setup test case
            """
            self.collection = EffectsCollection()
    
        def test_adding_effect_handle(self):
            """
            Test that effect handle can be added and retrieved
            """
            handle = EffectHandleBuilder().build()

            self.collection.add_effect_handle(handle)

            assert_that(self.collection, has_effect_handle(handle))

    test_class = TestEffectsCollection()
    test_class.setup()
    test_class.test_adding_effect_handle()

Interesting parts of the test are especially the usage of EffectHandleBuilder
to create the EffectHandle object and the customer has_effect_handle matcher.

Builders are used because they make setting up objects easy, especially when
dealing with very complex objects (Character for example). They are placed
at :py:mod:`pyherc.test.builders` module.

Custom matchers are used because they make dealing with verification somewhat 
cleaner. If the internal implementation of class changes, we need to only 
change how builders construct it and how matchers match it and tests should not
need any modifications. Custom matchers can be found at 
:py:mod:`pyherc.test.matchers` module.

Cutesy
------
Cutesy is an internal domain specific language. Basically, it's just a 
collection of functions that can be used to contruct nice looking tests. Theory
is that these easy to read tests can be used to communicate what the system
is supposed to be doing on a high level, without making things complicated
with all the technical details.

Here's an example, how to test that getting hit will cause hit points to go
down.

.. testcode::

    from pyherc.test.cutesy.dictionary import strong, Adventurer
    from pyherc.test.cutesy.dictionary import weak, Goblin
    from pyherc.test.cutesy.dictionary import Level

    from pyherc.test.cutesy.dictionary import place, middle_of
    from pyherc.test.cutesy.dictionary import right_of
    from pyherc.test.cutesy.dictionary import make,  hit

    from hamcrest import assert_that
    from pyherc.test.cutesy.dictionary import has_less_hit_points

    class TestCombatBehaviour():
    
        def test_hitting_reduces_hit_points(self):
            Pete = strong(Adventurer())
            Uglak = weak(Goblin())

            place(Uglak, middle_of(Level()))
            place(Pete, right_of(Uglak))

            make(Uglak, hit(Pete))

            assert_that(Pete, has_less_hit_points())
        
    test = TestCombatBehaviour()
    test.test_hitting_reduces_hit_points()

Tests written with Cutesy follow same guidelines as regular unit tests. However
they are placed in package :py:mod:`pyherc.test.bdd`
    
Doctest
-------
Doctest tests are written inside of .rst documents that are used to generate
documentation (including this one you are currently reading). These documents
are placed in doc/api/source folder and folders inside it.

``.. testcode::`` Starts test code block. Code example is placed inside this
one.

``.. testoutput::`` Is optional block. It can be omitted if it is enough to see
that the code example can be executed. If output of the example needs to be
verified, expected output is placed here.

Nosetest example earlier in this document is also a doctest example. If you
view source of this page, you can see how it has been constructed.

More information can be found at 
`Sphinx documentation <http://sphinx.pocoo.org/ext/doctest.html>`_.

Behave
------
Tests with behave are placed under directory behave/features. They consists of
two parts: feature-file specifying one or more test scenarios and python
implementation of steps in feature-files.

The earlier Cutesy example can be translated to behave as follows::

    Feature: Combat
      as an character
      in order to kill enemies
      I want to damage my enemies
    
      Scenario: hit in unarmed combat
         Given Pete is Adventurer
           And Uglak is Goblin
           And Uglak is standing in room
           And Pete is standing next to Uglak     
          When Uglak hits Pete
          Then Pete should have less hitpoints
          
Each of the steps need to be defined as Python code::

    @given(u'{character_name} is Adventurer')
    def impl(context, character_name):
        if not hasattr(context, 'characters'):
            context.characters = []
        new_character = Adventurer()
        new_character.name = character_name
        context.characters.append(new_character)

It is advisable not to reimplement all the logic in behave tests, but reuse
existing functionality from Cutesy. This makes tests both faster to write and
easier to maintain. For more information on using behave, have a look at their
online tutorial_.
        
.. _nose: https://github.com/nose-devs/nose/
.. _doctest: http://docs.python.org/library/doctest.html
.. _behave: http://pypi.python.org/pypi/behave
.. _mockito-python: http://code.google.com/p/mockito-python/
.. _pyhamcrest: http://pypi.python.org/pypi/PyHamcrest
.. _nosy: http://pypi.python.org/pypi/nosy
.. _tutorial: http://packages.python.org/behave/tutorial.html
