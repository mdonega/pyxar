import cmd
import os
import readline

class exit_cmd(cmd.Cmd, object):
    def can_exit(self):
        return True
    def onecmd(self, line):
        r = super (exit_cmd, self).onecmd(line)
        if r and (self.can_exit() or
           raw_input('exit anyway ? (yes/no):')=='yes'):
             return True
        return False
    def do_exit(self, s):
        return True
    def help_exit(self):
        print "Exit the interpreter."
        print "You can also use the Ctrl-D shortcut."
    do_EOF = do_exit
    help_EOF= help_exit

class shell_cmd(exit_cmd, object):
    def do_shell(self, s):
        os.system(s)
    def help_shell(self):
        print "execute shell commands"

class CmdTB(shell_cmd, object):
    def __init__(self):
        super(CmdTB, self).__init__()
        self.TB = ['ia','id','init_dut','set_dac']
        self.DUT = []
        #TODO, get rid of this, needed on OSX109
        if 'libedit' in readline.__doc__:
            readline.parse_and_bind("bind ^I rl_complete")
        else:
            readline.parse_and_bind("tab: complete")
    
    def complete_tb(self, text, line, begidx, endidx):
        if not text:
            completions = self.TB[:]
        else:
            completions = [ f
                            for f in self.TB
                            if f.startswith(text)
                            ]
        return completions
    
    def do_tb(self, line):
        args = line.split()
        for arg in args[1:]:
            try: 
                arg = int(arg)
            except ValueError:
                pass
        try:
            getattr(self.tb, args[0])(*args[1:])
        except:
            print 'wrong command'

    def complete_dut(self, text, line, begidx, endidx):
        if not text:
            completions = self.DUT[:]
        else:
            completions = [ f
                            for f in self.DUT
                            if f.startswith(text)
                            ]
        return completions
    
    def do_dut(self, line):
        args = line.split()
        for arg in args[1:]:
            try: 
                arg = int(arg)
            except ValueError:
                pass
        try:
            getattr(self.tb.dut, args[0])(*args[1:])
        except:
            print 'wrong command'


class PyCmd(CmdTB, object):
    """Simple command processor example."""
    def __init__(self):
        super(PyCmd, self).__init__()
        self.prompt = 'pyXar > '
        self.directory = 'data'

        tests = ['Calibrate', 'PHMap', 'Threshold', 'BondMap', 'Trim', 'TrimBits', 'Pretest', 'SCurves', 'PHCalibration', 'HRMap']

        # dinamicaly generate the help and do class methods for the tests
        for test in tests:
            self._do_factory(test)
            self._help_factory(test)

    def _do_factory(self, test):
        def _do_test(self, line):
            self.run_test(test)
        _do_test.__name__ = 'do_%s'%test
        setattr(self.__class__,_do_test.__name__,_do_test)

    def _help_factory(self, test):
        def _help_test(self):
            print self.get_help(test)
        _help_test.__name__ = 'help_%s'%test
        setattr(self.__class__,_help_test.__name__,_help_test)

    def help_init(self):
        print "Initialize DUT and TB as specified in module and tb config."

    def do_DacDac(self, line):
        #TODO Expose to cui
        self.dut.roc(0).pixel(5,5).active = True
        #self.dut.roc(1).pixel(5,5).active = True
        self.run_test('DacDac')
    
    def do_PHScan(self, line):
        #TODO Expose to cui
        self.dut.roc(0).pixel(5,5).active = True
        #self.dut.roc(0).pixel(15,15).active = True
        #self.dut.roc(1).pixel(5,5).active = True
        self.run_test('PHScan')

    def do_FullTest(self, line):
        self.run_test('Calibrate')
        self.run_test('BondMap')
        self.run_test('SCurves')
        self.run_test('PHCalibration')
        self.run_test('Trim')
