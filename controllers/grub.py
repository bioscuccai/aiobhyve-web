class GrubView(web.View):
  @aiohttp_jinja2.template('/grub/new.html')
  def get(self):
    isos = glob.glob('/usr/iso/*.iso')
    disks = glob.glob('/usr/vms/**/*.img')
    disks.extend(glob.glob('/dev/zvol/**/*'))

    form = forms.GrubForm()
    form.isos.choices = [(iso, iso) for iso in isos]
    form.disks.choices = [(disk, disk) for disk in disks]
    return locals()

  async def post(self):
    body = await self.request.post()

    isos = glob.glob('/usr/iso/*.iso')
    disks = glob.glob('/usr/vms/**/*.img')
    disks.extend(glob.glob('/dev/zvol/**/*'))

    form = forms.GrubForm(body)
    form.isos.choices = [(iso, iso) for iso in isos]
    form.disks.choices = [(disk, disk) for disk in disks]
    if form.validate():
      command = await runners.grub.run_command(**form.data)
      if form.data['debug']:
        return aiohttp_jinja2.render_template('/grub/debug.html', self.request, locals())
    return web.HTTPFound(self.request.app.router['vms_new'].url_for().with_query(
      name=form.data['name'],
      memory=form.data['memory']
    ))
