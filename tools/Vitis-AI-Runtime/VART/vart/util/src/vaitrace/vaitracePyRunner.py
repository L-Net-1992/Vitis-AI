#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# Copyright 2019 Xilinx Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import sys
import time
import signal
from multiprocessing import Process

import collector
import tracer
import logging

pyProc = None

def pyRunCtx(pyCmd):
    sys.argv[:] = pyCmd
    progname = pyCmd[0]
    sys.path.insert(0, os.path.dirname(progname))

    logging.info("Vaitrace compile python code: %s" % progname)

    with open(progname, 'rb') as fp:
        code = compile(fp.read(), progname, 'exec')

    globs = {
        '__file__': progname,
        '__name__': '__main__',
        '__package__': None,
        '__cached__': None,
    }

    logging.info("Vaitrace exec poython code: %s" % progname)

    exec(code, globs, None)

def handler(signum, frame):
    global pyProc

    if pyProc.is_alive():
        pyProc.kill()
        logging.info("Killing process...")
        logging.info("Processing trace data, please wait...")
    else:
        logging.info("Processing trace data, please wait...")

def run(globalOptions: dict):
    global pyProc

    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)

    options = globalOptions

    if options.get('cmdline_args').get('bypass', False):
        cmd = options.get('control').get('cmd')
        logging.info("Bypass vaitrace, just run cmd")

        pyCmd = options.get('control').get('cmd')
        pyRunCtx(pyCmd)
        exit(0)

    """Preparing"""
    tracer.prepare(options)
    tracer.start()

    """requirememt format: ["tracerName", "tracerName1", "hwInfo", ...]"""
    collector.prepare(options, tracer.getSourceRequirement())
    collector.start()

    """Start Running"""
    pyCmd = options.get('control').get('cmd')
    timeout = options.get('control').get('timeout')

    #pyRunCtx(pyCmd)
    pyProc = Process(target=pyRunCtx, args=(pyCmd,))
    pyProc.start()

    options['control']['launcher'] = "python"
    options['control']['pid'] = pyProc.pid
    options['control']['time'] = time.strftime(
        "%Y-%m-%d %H:%M:%S", time.localtime())
    
    if timeout <= 0:
        pyProc.join()
    else:
       while timeout > 0:
           time.sleep(1)
           timeout -= 1
           p = pyProc.is_alive()
           if p == False:
               break
    
    collector.stop()
    tracer.stop()
    # pyProc.join()

    tracer.process(collector.getData())