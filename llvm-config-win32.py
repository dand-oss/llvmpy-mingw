import sys, os

def find_path_of(filename, envvar='PATH'):
    """Finds the path from $PATH where the file exists, returns None if not found."""
    pathlist = os.getenv(envvar).split(os.pathsep)
    for path in pathlist:
        if os.path.exists(os.path.join(path, filename)):
            return os.path.abspath(path)
    return None

if sys.argv[1] == '--version':
    cmd = 'llvm-tblgen --version'
    # Hardcoded extraction, only tested on llvm 3.1
    result = os.popen(cmd).read().split('\n')[1].strip().split(' ')[2]
    print result
elif sys.argv[1] == '--ldflags':
    for ldflag in """
imagehlp
psapi
""".split():
        print('-l%s' % ldflag)
elif sys.argv[1] == '--libs':
    # NOTE: instead of actually looking at the components requested,
    #       we just spit out a bunch of libs
    for lib in """
LLVMNVPTXCodeGen
LLVMNVPTXDesc
LLVMNVPTXInfo
LLVMNVPTXAsmPrinter
LLVMLinker
LLVMArchive
LLVMAsmParser
LLVMipo
LLVMVectorize
LLVMInstrumentation
LLVMBitWriter
LLVMBitReader
LLVMInterpreter
LLVMX86Disassembler
LLVMX86CodeGen
LLVMSelectionDAG
LLVMAsmPrinter
LLVMX86AsmParser
LLVMMCParser
LLVMX86Desc
LLVMX86AsmPrinter
LLVMX86Utils
LLVMX86Info
LLVMJIT
LLVMRuntimeDyld
LLVMCodeGen
LLVMExecutionEngine
LLVMScalarOpts
LLVMInstCombine
LLVMTransformUtils
LLVMipa
LLVMAnalysis
LLVMTarget
LLVMMC
LLVMObject
LLVMCore
LLVMSupport
""".split():
        print('-l%s' % lib)
        # Look for the PTX .lib in %LIBPATH%
        if find_path_of('LLVMPTXCodeGen.lib', 'LIBPATH') != None:
            print('-lLLVMPTXAsmPrinter')
            print('-lLLVMPTXCodeGen')
            print('-lLLVMPTXDesc')
            print('-lLLVMPTXInfo')
elif sys.argv[1] == '--includedir': 
    llvmbin = find_path_of('llvm-tblgen.exe')
    if llvmbin is None:
        raise RuntimeError('Could not find LLVM')
    incdir = os.path.abspath(os.path.join(llvmbin, '../include'))
    if not os.path.exists(os.path.join(incdir, 'llvm/BasicBlock.h')):
        raise RuntimeError('Could not find LLVM include dir')
    print incdir
elif sys.argv[1] == '--libdir': 
    llvmbin = find_path_of('llvm-tblgen.exe')
    if llvmbin is None:
        raise RuntimeError('Could not find LLVM')
    libdir = os.path.abspath(os.path.join(llvmbin, '../lib'))
    if not os.path.exists(os.path.join(libdir, 'libLLVMCore.a')):
        raise RuntimeError('Could not find LLVM lib dir')
    print libdir
else:
    raise RuntimeError('Unrecognized llvm-config command %s' % sys.argv[1])
