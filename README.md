# pycparser v2.19

Pycparser是C语言的解析器，支持完整的C99标准，用纯Python编写。

非常方便对C语言源码的解析和处理，如生成AST、提取源码中函数调用关系等。

[扩展版本pycparserext 支持gun扩展 和 opencl ](https://github.com/Ewenwan/pycparserext)


:Author: `Eli Bendersky <https://eli.thegreenplace.net/>`_


.. contents::
    :backlinks: none

.. sectnum::


简介 Introduction
============

什么是 What is pycparser?
------------------

**pycparser** is a parser for the C language, written in pure Python. It is a
module designed to be easily integrated into applications that need to parse
C source code.

pycparser 是用纯 python 编写的C 语言解析器。 它是一个设计成易于集成到需要解析C 源代码的应用程序的MODULE。

What is it good for? 有什么好处？
--------------------

Anything that needs C code to be parsed. The following are some uses for
**pycparser**, taken from real user reports:

需要解析C 代码的任何内容。 以下是从实际用户报告中获取的pycparser的一些用法：

C 代码混淆程序

各种专用C 编译器前端

static 代码检查器

自动化单元测试

向C 语言添加专用扩展

* C code obfuscator
* Front-end for various specialized C compilers
* Static code checker
* Automatic unit-test discovery
* Adding specialized extensions to the C language

One of the most popular uses of **pycparser** is in the `cffi
<https://cffi.readthedocs.io/en/latest/>`_ library, which uses it to parse the
declarations of C functions and types in order to auto-generate FFIs.

cffi命令行库，它使用它来解析C 函数和类型的声明以便自动生成 FFIs。

**pycparser** is unique in the sense that it's written in pure Python - a very
high level language that's easy to experiment with and tweak. To people familiar
with Lex and Yacc, **pycparser**'s code will be simple to understand. It also
has no external dependencies (except for a Python interpreter), making it very
simple to install and deploy.

这是一种非常高级的语言，可以轻松地进行实验和调整。

它还没有外部依赖项( 除了 python 解释器)，这使得安装和部署它变得非常简单。

Which version of C does pycparser support?  pycparser支持的版本？
------------------------------------------

**pycparser** aims to support the full C99 language (according to the standard
ISO/IEC 9899). Some features from C11 are also supported, and patches to support
more are welcome.

pycparser 旨在支持完整的c 语言语言( 根据标准 ISO/IEC 9899 )。 C11还支持一些特性，欢迎使用支持更多的补丁。
尽管花费了很高的代价，但是它可以很容易地把代码解析成许多 GCC-isms。 有关详细信息，


**pycparser** supports very few GCC extensions, but it's fairly easy to set
things up so that it parses code with a lot of GCC-isms successfully. See the
`FAQ <https://github.com/eliben/pycparser/wiki/FAQ>`_ for more details.

What grammar does pycparser follow?
-----------------------------------

**pycparser** very closely follows the C grammar provided in Annex A of the C99
standard (ISO/IEC 9899).

How is pycparser licensed?
--------------------------

`BSD license <https://github.com/eliben/pycparser/blob/master/LICENSE>`_.

Contact details
---------------

For reporting problems with **pycparser** or submitting feature requests, please
open an `issue <https://github.com/eliben/pycparser/issues>`_, or submit a
pull request.


Installing
==========

Prerequisites
-------------

* **pycparser** was tested on Python 2.7, 3.4-3.6, on both Linux and
  Windows. It should work on any later version (in both the 2.x and 3.x lines)
  as well.
  
  在Linux和 Windows 上的python 2.7，3.3-3.6进行了测试

* **pycparser** has no external dependencies. The only non-stdlib library it
  uses is PLY, which is bundled in ``pycparser/ply``. The current PLY version is
  3.10, retrieved from `<http://www.dabeaz.com/ply/>`_

pycparser 没有外部依赖项。 它使用的惟一非stdlib库是 PLY，它捆绑在 pycparser/ply 中。

Note that **pycparser** (and PLY) uses docstrings for grammar specifications.
Python installations that strip docstrings (such as when using the Python
``-OO`` option) will fail to instantiate and use **pycparser**. You can try to
work around this problem by making sure the PLY parsing tables are pre-generated
in normal mode; this isn't an officially supported/tested mode of operation,
though.

Installation process
--------------------

安装 pycparser 非常简单。 下载并解压包之后，你只需执行标准的python setup.py install。 安装脚本将把 pycparser MODULE 放入 python 库安装中的site-packages 中。

Installing **pycparser** is very simple. Once you download and unzip the
package, you just have to execute the standard ``python setup.py install``. The
setup script will then place the ``pycparser`` module into ``site-packages`` in
your Python's installation library.

Alternatively, since **pycparser** is listed in the `Python Package Index
<https://pypi.org/project/pycparser/>`_ (PyPI), you can install it using your
favorite Python packaging/distribution tool, for example with::

    > pip install pycparser

Known problems
--------------

* Some users who've installed a new version of **pycparser** over an existing
  version ran into a problem using the newly installed library. This has to do
  with parse tables staying around as ``.pyc`` files from the older version. If
  you see unexplained errors from **pycparser** after an upgrade, remove it (by
  deleting the ``pycparser`` directory in your Python's ``site-packages``, or
  wherever you installed it) and install again.


Using
=====

Interaction with the C preprocessor  与C 预处理器的交互 
-----------------------------------

In order to be compilable, C code must be preprocessed by the C preprocessor -
``cpp``. ``cpp`` handles preprocessing directives like ``#include`` and
``#define``, removes comments, and performs other minor tasks that prepare the C
code for compilation.

For all but the most trivial snippets of C code **pycparser**, like a C
compiler, must receive preprocessed C code in order to function correctly. If
you import the top-level ``parse_file`` function from the **pycparser** package,
it will interact with ``cpp`` for you, as long as it's in your PATH, or you
provide a path to it.

Note also that you can use ``gcc -E`` or ``clang -E`` instead of ``cpp``. See
the ``using_gcc_E_libc.py`` example for more details. Windows users can download
and install a binary build of Clang for Windows `from this website
<http://llvm.org/releases/download.html>`_.

为了编译，C 代码必须由C 预处理器( cpp 预处理器) 预处理。 cpp 处理类似 #include 和 #define的预处理指令，删除注释，并执行它的他编译C 代码的小任务。
除了最琐碎的C 代码 Fragment ( 比如C 编译器)，就必须接收预处理的C 代码才能正常工作。 在你的路径中输入顶级 parse_file 函数，它将与 cpp 交互，只要它在你的路径中，或者你提供了一条路径到它。

请注意，你可以使用 gcc -E 或者 clang -E 而不是 cpp。 有关更多详细信息，请参见 using_gcc_E_libc.py 示例。 Windows 用户可以下载并安装一个二进制构建的Clang，从这个网站的


What about the standard C library headers? 标准的C依赖库 如何？
------------------------------------------

C code almost always ``#include``\s various header files from the standard C
library, like ``stdio.h``. While (with some effort) **pycparser** can be made to
parse the standard headers from any C compiler, it's much simpler to use the
provided "fake" standard  includes in ``utils/fake_libc_include``. These are
standard C header files that contain only the bare necessities to allow valid
parsing of the files that use them. As a bonus, since they're minimal, it can
significantly improve the performance of parsing large C files.

The key point to understand here is that **pycparser** doesn't really care about
the semantics of types. It only needs to know whether some token encountered in
the source is a previously defined type. This is essential in order to be able
to parse C correctly.

See `this blog post
<https://eli.thegreenplace.net/2015/on-parsing-c-type-declarations-and-fake-headers>`_
for more details.

Basic usage
-----------

Take a look at the |examples|_ directory of the distribution for a few examples
of using **pycparser**. These should be enough to get you started. Please note
that most realistic C code samples would require running the C preprocessor
before passing the code to **pycparser**; see the previous sections for more
details.

.. |examples| replace:: ``examples``
.. _examples: examples


Advanced usage
--------------

The public interface of **pycparser** is well documented with comments in
``pycparser/c_parser.py``. For a detailed overview of the various AST nodes
created by the parser, see ``pycparser/_c_ast.cfg``.

There's also a `FAQ available here <https://github.com/eliben/pycparser/wiki/FAQ>`_.
In any case, you can always drop me an `email <eliben@gmail.com>`_ for help.


Modifying   修改需关注 _c_ast.cfg  和 _ast_gen.py
=========

There are a few points to keep in mind when modifying **pycparser**:

* The code for **pycparser**'s AST nodes is automatically generated from a
  configuration file - ``_c_ast.cfg``, by ``_ast_gen.py``. If you modify the AST
  configuration, make sure to re-generate the code.
* Make sure you understand the optimized mode of **pycparser** - for that you
  must read the docstring in the constructor of the ``CParser`` class. For
  development you should create the parser without optimizations, so that it
  will regenerate the Yacc and Lex tables when you change the grammar.


Package contents
================

Once you unzip the ``pycparser`` package, you'll see the following files and
directories:

README.rst:
  This README file.

LICENSE:
  The pycparser license

setup.py:
  Installation script

examples/:
  A directory with some examples of using **pycparser**

pycparser/:
  The **pycparser** module source code.

tests/:
  Unit tests.

utils/fake_libc_include:
  Minimal standard C library include files that should allow to parse any C code.

utils/internal/:
  Internal utilities for my own use. You probably don't need them.


Contributors
============

Some people have contributed to **pycparser** by opening issues on bugs they've
found and/or submitting patches. The list of contributors is in the CONTRIBUTORS
file in the source distribution. After **pycparser** moved to Github I stopped
updating this list because Github does a much better job at tracking
contributions.


CI Status
=========

**pycparser** has automatic testing enabled through the convenient
`Travis CI project <https://travis-ci.org>`_. Here is the latest build status:

.. image:: https://travis-ci.org/eliben/pycparser.png?branch=master
  :align: center
  :target: https://travis-ci.org/eliben/pycparser

AppVeyor also helps run tests on Windows:

.. image:: https://ci.appveyor.com/api/projects/status/wrup68o5y8nuk1i9?svg=true
  :align: center
  :target: https://ci.appveyor.com/project/eliben/pycparser/
