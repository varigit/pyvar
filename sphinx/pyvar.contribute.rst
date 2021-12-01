Contribute
==========

This project is still under development and we encourage you to contribute
to the project. Please see below our contributing guide for more details:

Coding Convention and Requirements
----------------------------------

*  Write object-oriented code. This has the advantages of data hiding and modularity. It allows reusability, modularity, polymorphism, data encapsulation, and inheritance.

   *  You must write modular and non-repetitive code;
   *  You must use classes and methods in your code.

*  Write the code according to PEP 8. For more information, read the `PEP 8`_ page.

   *  This package uses *snake_case* for variables, functions, methods, and modules or packages names.

*  Each feature should come with test cases that can be executed as unit tests during build.

*  Each feature should come with small codes for executing the classes and functions.

*  Avoid as much as you can adding dependencies that are not currently supported by Variscite BSP.

   *  You must handle this as optional feature using accert or try methods to verify if it is installed or not.

*  Before sending the pull request or patch follow the above recommendations:

   *  You must keep your code clean and neat, which means that must be readable;
   *  You must not apply general rules of git commits and common senses;
   *  You must not write a lengthy commit - only one single topic per commit;
   *  You must provide enough background information and references.

.. _PEP 8: https://www.python.org/dev/peps/pep-0008/

Signing-off Commits
-------------------

Each commit is required to be *signed-off* by the corresponding author. Please
configure your development environment with your information:

.. code-block:: bash

    $ git config --global user.name "Your Name"
    $ git config --global user.email "Your E-mail"

Add sign-off for a commit with **-s** option. See an example below:

.. code-block:: bash

    $ git add <file_name>
    $ git commit -s // -s (--signoff) means automated signed-off-by statement.
    
    
Including a "Signed-off-by:" tag in your commit means that you are making the Developer Certificate of Origin (DCO) certification for that commit.

* A copy of the DCO text can be found at `Developer Certificate`_.

.. _Developer Certificate: https://developercertificate.org/

Code Reviews, Pull Requests and Patches
---------------------------------------

*  The patches or pull requests are reviewed by the maintainers, committers and reviewers.

*  If you are a committer or a reviewer of the specific component, you are:

   *  Obligated to review incoming related pull requests or patches;
   *  Obligated to give feedback on pull requests or patches especially on similar topics/components.


Merge Criteria
~~~~~~~~~~~~~~

A pull request must be according to the following statements to be accepted:

*  Passed all the tests executed for the any other code reviewer.

   *  This includes unit tests and integration tests;
   *  If the pull requests affects sensitive codes or may affect wide ranges of components, reviewers will wait for other reviewers to back them up;
   *  If the pull request is messy, you will need to wait indefinitely to get reviews.

*  There is no rejections from any official reviewers.
*  There is no pending negative feed-backs (unresolved issues) from reviewers.

After these above requirements, then a committer with merging privilege will be able to merge the given pull request or patch.
