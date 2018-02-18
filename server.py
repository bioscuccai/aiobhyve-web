from aiohttp import web
import glob

import config
import aiohttp_jinja2
import jinja2
import os
import itertools
import parsers.vm_list
import parsers.dnsmasq
import parsers.bhyve_parser

import runners.bhyvectl
import runners.bhyve
import runners.bhyveload
import runners.grub
import runners.ifconfig
import forms

class MainView(web.View):
  @aiohttp_jinja2.template('main.html')
  async def get(self):
    return

class ListView(web.View):
  @aiohttp_jinja2.template('vms/vm_list.html')
  async def get(self):
    vms = parsers.vm_list.list_vms()
    return locals()
  
  async def post(self):
    body = await self.request.post()

    isos = glob.glob('/usr/iso/*.iso')
    disks = glob.glob('/usr/vms/**/*.img')
    disks.extend(glob.glob('/dev/zvol/**/*'))

    form = forms.VmForm(body)
    form.isos.choices = [(iso, iso) for iso in isos]
    form.disks.choices = [(disk, disk) for disk in disks]
    form.tap.choices = runners.ifconfig.tap_choices(runners.ifconfig.all_taps())

    if form.validate():
      vm = runners.bhyve.BhyveVm(**form.data)
      print(vm)
      command = runners.bhyve.create_command(vm)
      print(command)

      if form.data['debug']:
        return aiohttp_jinja2.render_template('/vms/vm_debug.html', self.request, locals())
      await runners.bhyve.run_vm(vm)
    else:
      print(form.errors)
    return web.HTTPFound(self.request.app.router['vms'].url_for().with_query({"name": form.data['name']}))

class VmShow(web.View):
  @aiohttp_jinja2.template('/vms/vm_show.html')
  async def get(self):
    name = self.request.match_info.get('name')
    stats_raw = await runners.bhyvectl.get_status(name)
    stats = parsers.bhyve_parser.parse_stats(stats_raw)
    return locals()

  async def post(self):
    pass

class VmNew(web.View):
  @aiohttp_jinja2.template('/vms/vm_new.html')
  async def get(self):
    isos = glob.glob('/usr/iso/*.iso')
    disks = glob.glob('/usr/vms/**/*.img')
    disks.extend(glob.glob('/dev/zvol/**/*'))
    taps = runners.ifconfig.all_taps()

    prefilled_fields = {
      "name": self.request.query.get("name", ""),
      "isos": [],
      "disks": []
    }
    
    if 'image' in self.request.query:
      if self.request.query['image'] in isos:
        prefilled_fields['isos'].append(self.request.query['image'])
      if self.request.query['image'] in disks:
        prefilled_fields['disks'].append(self.request.query['image'])
    
    if 'selected_disks' in self.request.query:
      selected_disks = self.request.query['selected_disks'].split(',')
      prefilled_fields["disks"].extend(selected_disks)

    if 'selected_isos' in self.request.query:
      selected_isos = self.request.query['selected_isos'].split(',')
      prefilled_fields["isos"].extend(selected_isos)

    form = forms.VmForm(data=prefilled_fields)
    form.isos.choices = [(iso, iso) for iso in isos]
    form.disks.choices = [(disk, disk) for disk in disks]
    form.tap.choices = runners.ifconfig.tap_choices(runners.ifconfig.all_taps())
    return locals()

class LeaseList(web.View):
  @aiohttp_jinja2.template('dnsmasq/lease_list.html')
  def get(self):
    leases = parsers.dnsmasq.list_leases()
    return locals()

class BhyveLoadView(web.View):
  @aiohttp_jinja2.template('/bhyveload/new.html')
  async def get(self):
    isos = glob.glob('/usr/iso/*.iso')
    disks = glob.glob('/usr/vms/**/*.img')
    images = [*isos, *disks]
    form = forms.BhyveLoadForm()
    form.image.choices = [(image, image) for image in images]
    return locals()
  
  async def post(self):
    body = await self.request.post()

    isos = glob.glob('/usr/iso/*.iso')
    disks = glob.glob('/usr/vms/**/*.img')
    disks.extend(glob.glob('/dev/zvol/**/*'))

    images = [*isos, *disks]
    form = forms.BhyveLoadForm()
    form = forms.BhyveLoadForm(body)
    form.image.choices = [(image, image) for image in images]

    if form.validate():
      (out, err) = await runners.bhyveload.load_image(
        name = form.data['name'],
        memory = form.data['memory'],
        console = form.data['console'],
        image = form.data['image']
      )
    return web.HTTPFound(self.request.app.router['vms_new'].url_for().with_query(
      name=form.data['name'],
      memory=form.data['memory'],
      console=form.data['console'],
      image=form.data['image']
    ))

class PoweroffView(web.View):
  async def get(self):
    await runners.bhyvectl.poweroff(self.request.match_info.get('name'))
    return web.HTTPFound(self.request.app.router['vms'].url_for())

class DestroyView(web.View):
  async def get(self):
    await runners.bhyvectl.destroy(self.request.match_info.get('name'))
    return web.HTTPFound(self.request.app.router['vms'].url_for())

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
      memory=form.data['memory'],
      selected_disks = ','.join(form.data['disks']),
      selected_isos = ','.join(form.data['isos'])
    ))

def setup_routes(app):
  app.router.add_route('*', '/', MainView)
  app.router.add_route('*', '/vms', ListView, name='vms')
  app.router.add_route('*', '/vms/new', VmNew, name='vms_new')
  app.router.add_route('*', '/vms/{name}', VmShow)
  app.router.add_route('*', '/vms/{name}/poweroff', PoweroffView)
  app.router.add_route('*', '/vms/{name}/destroy', DestroyView)
  app.router.add_route('*', '/dnsmasq', LeaseList, name='leases')
  app.router.add_route('*', '/bhyveload', BhyveLoadView, name='bhyveload')
  app.router.add_route('*', '/grub', GrubView, name='grub')

if __name__ == '__main__':
  app = web.Application(debug=True)
  aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
  setup_routes(app)
  web.run_app(app, port=8081)
