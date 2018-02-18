from wtforms import Form, StringField, BooleanField, IntegerField, SelectField, SelectMultipleField

class VmForm(Form):
    name = StringField()
    memory = IntegerField(default=1024)
    cores = IntegerField(default=1)
    framebuffer = IntegerField(default=5902)
    bios = SelectField(choices=[('', 'none'), ('uefi', 'uefi'), ('csm', 'csm')])
    loader = SelectField(choices=[('grub', 'grub'), ('bhyveload', 'bhyveload'), ('bootrom', 'bootrom')])
    hostbridge = BooleanField(default=True)
    tap = SelectField(choices=[])
    #tap = StringField(default="tap2")
    
    isos = SelectMultipleField(choices=[])
    disks = SelectMultipleField(choices=[])
    console = StringField(default="/dev/nmdm1B")
    enable_framebuffer = BooleanField(default=False)
    vnc_wait = BooleanField(default=False)
    debug = BooleanField(default=False)
    hostbridge_type = SelectField(choices=[('default', 'default'), ('amd', 'AMD')])

class BhyveLoadForm(Form):
    name = StringField()
    memory = IntegerField(default=1024)
    console = StringField(default="/dev/nmdm1B")
    image = SelectField(choices=[])
    auto_enter = BooleanField(default=True)

class GrubForm(Form):
    name = StringField()
    memory = IntegerField(default=1024)
    root_device = StringField(default="cd0")
    isos = SelectMultipleField(choices=[])
    disks = SelectMultipleField(choices=[])
    command = StringField()
    debug = BooleanField(default=False)
    preset = SelectField(choices = [('empty', 'Empty'), ('netbsd-cd', 'NetBSD CD'), ('netbsd-hd', 'NetBSD HD'), ('openbsd-cd', 'OpenBSD CD'), ('openbsd-hd', 'OpenBSD HD')])
