<table>
  <tr>
    <td colspan=2><strong>
    pynchon
      </strong>&nbsp;&nbsp;&nbsp;&nbsp;
    </td>
  </tr>
  <tr>
    <td width=15%><img src=img/icon.png style="width:150px"></td>
    <td>
      <br/><br/>
      <a href=https://pypi.python.org/pypi/pynchon/><img src="https://img.shields.io/pypi/l/pynchon.svg"></a>
      <a href=https://pypi.python.org/pypi/pynchon/><img src="https://badge.fury.io/py/pynchon.svg"></a>
      <a href="https://github.com/elo-enterprises/pynchon/actions/workflows/python-publish.yml"><img src="https://github.com/elo-enterprises/pynchon/actions/workflows/python-publish.yml/badge.svg"></a><a href="https://github.com/elo-enterprises/pynchon/actions/workflows/python-test.yml"><img src="https://github.com/elo-enterprises/pynchon/actions/workflows/python-test.yml/badge.svg"></a>
    </td>
  </tr>
</table>

---------------------------------------------------------------------------------

<div class="toc">
<ul>
<li><a href="#overview">Overview</a></li>
<li><a href="#features">Features</a></li>
<li><a href="#quick-start">Quick Start</a></li>
</ul>
</div>


---------------------------------------------------------------------------------

## Overview

Pynchon is a library, tool, and extensible framework for documentation and project management.  It's useful in general, but specializes in autogenerating documentation for python projects.

This code is still experimental and interface stability is not yet guaranteed.. make sure to pin pynchon at specific versions in your project.

## Features

* Terraform-style plan/apply workflows, with support for parallel execution
* Plugin framework for extensions
* Support for tools like [Jinja](#), Markdown, [Mermaid](#) and [pandoc](#)
* Friendly output for machines and for humans

## Quick Start

Pynchon is on PyPI, so to get the latest:

```bash
pip install pynchon
```

Or, for developers:

```bash
# for ssh
git clone git@github.com:elo-enterprises/pynchon.git

# or for http
# git clone https://github.com/elo-enterprises/pynchon

cd pynchon
pip install -e .
```

---------------------------------------------------------------------------------
