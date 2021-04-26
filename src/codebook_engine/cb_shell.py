import uuid



class CbShell(object):
    
    _running = False

    def __init__(self):
        pass

    def run(self):
        self._running = True
        while self._running:
            cmd = input('>> ')
            exe = self.parse(cmd)
            if exe != None:
                self.execute(exe)

    def parse(self, cmd):
        li = cmd.split(' ')
        if li[0] == '':
            return
        if li[0] == 'train':
            return self.build_training_exe(li)
        elif li[0] == 'separate':
            return self.build_separate_exe(li)
        elif li[0] == 'help':
            self.print_help()
        elif li[0] == 'exit':
            print(' * goodbye')
            self._running = False
        else:
            print(' * invalid command')

    def execute(self, exe):
        if exe.cmd == 'train':
            pass
        elif exe.cmd == 'separate':
            pass

    def build_training_exe(self, li):
        index = 1
        exe = RunConfig()
        while index <= len(li):
            if li[index] == '--source':
                if index+1 >= len(li):
                    print(' * missing parameter value for [--source], please provide a value for this parameter')
                else:
                    exe.source = li[index+1]
            elif li[index] == '--name':
                if index+1 >= len(li):
                    print(' * missing parameter value for [--name], please provide a value for this parameter')
                else:
                    exe.name = li[index+1]
            elif li[index] == '--alpha':
                if index+1 >= len(li):
                    print(' * missing parameter value for [--name], please provide a value for this parameter, or omit')
                else:
                    exe.alpha = li[index+1]
            elif li[index] == '--beta':
                if index+1 >= len(li):
                    print(' * missing parameter value for [--name], please provide a value for this parameter, or omit')
                else:
                    exe.alpha = li[index+1]
            else:
                print(' * invalid parameter: [{}]'.format(li[index]))
                break
            index+=2
        if exe.source == '':
            print(' * missing required parameter [--source]')
            return
        if exe.name == '':
            print(' * missing required parameter [--name]')
            return
        return exe

    def build_separate_exe(self, li):
        index = 1
        exe = RunConfig()
        while index <= len(li):
            if li[index] == '--source':
                if index+1 >= len(li):
                    print(' * missing parameter value for [--source], please provide a value for this parameter')
                else:
                    exe.source = li[index+1]
            elif li[index] == '--model':
                if index+1 >= len(li):
                    print(' * missing parameter value for [--model], please provide a value for this parameter')
                else:
                    exe.model = li[index+1]
            elif li[index] == '--out':
                if index+1 >= len(li):
                    print(' * missing parameter value for [--out], please provide a value for this parameter')
                else:
                    exe.out = li[index+1]

    def print_help(self):
        print('\n * commands:')
        print('\n     `train`\n')
        print('         Description:')
        print('             Create a new codebook model.')
        print('         Parameters:')
        print('             --source [required, path to video file]')
        print('             --name [optional, name your model for easy identification')
        print('             --alpha [optional, default=0.7]')
        print('             --beta [optional, default=1.1]')
        print('\n     `separate`\n')
        print('         Description:')
        print('             Use an existing codebook model on a video file specified by the [--path] argument.')
        print('         Parameters:')
        print('             --source [required, path to video file]')
        print('             --model [required, model to be used]')
        print('             --out [required, name of the output file]')
        print('\n     `help`\n')
        print('         Description:')
        print('             List all commands and their arguments.')
        print('\n     `exit`\n')
        print('         Description:')
        print('             Exit the program.')


class RunConfig(object):

    cmd = ''
    name = str(uuid.uuid1()) + '.model'
    source = ''
    model = ''
    alpha = 0.7
    beta = 1.1
    out = str(uuid.uuid1())

    def __init__(self):
        pass