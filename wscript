def configure(ctx):
    ctx.recurse('js')


def build(ctx):
    ctx.recurse('js')

    ctx(
        features     = 'replacer',
        source       = ctx.path.make_node('index.html'),
        target       = ctx.path.get_bld().make_node('index.html'),
        install_path = '${PREFIX}'
    )

    ctx.install_files('${PREFIX}', 'index.html')
    ctx.install_files('${PREFIX}', 'robots.txt')
    ctx.install_files('${PREFIX}', 'favicon.ico')
    ctx.install_files('${PREFIX}', 'singletrack.html')
    ctx.install_files('${PREFIX}', ctx.path.ant_glob('css/*.css'), relative_trick=True)
    ctx.install_files('${PREFIX}', ctx.path.ant_glob('images/*.png'), relative_trick=True)
    ctx.install_files('${PREFIX}', ctx.path.ant_glob('images/*.jpg'), relative_trick=True)
    ctx.install_files('${PREFIX}', ctx.path.ant_glob('lib/**'), relative_trick=True)
    ctx.install_files('${PREFIX}', ctx.path.ant_glob('translations/*.json'), relative_trick=True)



from waflib import Task, TaskGen

@TaskGen.feature('replacer')
@TaskGen.before('process_source')
def replacer_hook(self):
    self.source = getattr(self, 'source', None)
    self.target = getattr(self, 'target', None)

    task = self.create_task('replacer', self.to_nodes(self.source), self.to_nodes(self.target))
    self.source = []

    inst_to = getattr(self, 'install_path', None)
    if inst_to:
        self.bld.install_files(inst_to, task.outputs[:])


class replacer(Task.Task):

    def run(self):
        fhIn  = open(self.inputs[0].abspath(), 'r')
        content = fhIn.read()
        fhIn.close()

        if self.env.NAME == 'debug':
            files1 = self.env.JSSTAGE1
            files2 = self.env.JSSTAGE2
        else:
            files1 = [self.env.JSSTAGE1NAME]
            files2 = [self.env.JSSTAGE2NAME]

        stage1 = ''
        for jsFile in files1:
            stage1 = stage1 + '<script type="text/javascript" src="js/' + jsFile + '"></script>\n'

        stage2 = ''
        for jsFile in files2:
            stage2 = stage2 + '<script type="text/javascript" src="js/' + jsFile + '"></script>\n'

        content = content.replace('{{stage1}}', stage1)
        content = content.replace('{{stage2}}', stage2)

        fhOut = open(self.outputs[0].abspath(), 'w')
        fhOut.write(content)
        fhOut.close()
