# This file was automatically created by FeynRules 2.3.24
# Mathematica version: 12.0.0 for Mac OS X x86 (64-bit) (April 7, 2019)
# Date: Wed 9 Jun 2021 22:04:10


from __future__ import division
from object_library import all_particles, Particle
import parameters as Param

import propagators as Prop

a = Particle(pdg_code = 22,
             name = 'a',
             antiname = 'a',
             spin = 3,
             color = 1,
             mass = Param.ZERO,
             width = Param.ZERO,
             texname = 'a',
             antitexname = 'a',
             charge = 0,
             BL = 0,
             GhostNumber = 0,
             LeptonNumber = 0,
             Y = 0)

Z = Particle(pdg_code = 23,
             name = 'Z',
             antiname = 'Z',
             spin = 3,
             color = 1,
             mass = Param.MZ,
             width = Param.WZ,
             texname = 'Z',
             antitexname = 'Z',
             charge = 0,
             BL = 0,
             GhostNumber = 0,
             LeptonNumber = 0,
             Y = 0)

W__plus__ = Particle(pdg_code = 24,
                     name = 'W+',
                     antiname = 'W-',
                     spin = 3,
                     color = 1,
                     mass = Param.MW,
                     width = Param.WW,
                     texname = 'W+',
                     antitexname = 'W-',
                     charge = 1,
                     BL = 0,
                     GhostNumber = 0,
                     LeptonNumber = 0,
                     Y = 0)

W__minus__ = W__plus__.anti()

g = Particle(pdg_code = 21,
             name = 'g',
             antiname = 'g',
             spin = 3,
             color = 8,
             mass = Param.ZERO,
             width = Param.ZERO,
             texname = 'g',
             antitexname = 'g',
             charge = 0,
             BL = 0,
             GhostNumber = 0,
             LeptonNumber = 0,
             Y = 0)

ghA = Particle(pdg_code = 9000001,
               name = 'ghA',
               antiname = 'ghA~',
               spin = -1,
               color = 1,
               mass = Param.ZERO,
               width = Param.ZERO,
               texname = 'ghA',
               antitexname = 'ghA~',
               charge = 0,
               BL = 0,
               GhostNumber = 1,
               LeptonNumber = 0,
               Y = 0)

ghA__tilde__ = ghA.anti()

ghZ = Particle(pdg_code = 9000002,
               name = 'ghZ',
               antiname = 'ghZ~',
               spin = -1,
               color = 1,
               mass = Param.MZ,
               width = Param.WZ,
               texname = 'ghZ',
               antitexname = 'ghZ~',
               charge = 0,
               BL = 0,
               GhostNumber = 1,
               LeptonNumber = 0,
               Y = 0)

ghZ__tilde__ = ghZ.anti()

ghWp = Particle(pdg_code = 9000003,
                name = 'ghWp',
                antiname = 'ghWp~',
                spin = -1,
                color = 1,
                mass = Param.MW,
                width = Param.WW,
                texname = 'ghWp',
                antitexname = 'ghWp~',
                charge = 1,
                BL = 0,
                GhostNumber = 1,
                LeptonNumber = 0,
                Y = 0)

ghWp__tilde__ = ghWp.anti()

ghWm = Particle(pdg_code = 9000004,
                name = 'ghWm',
                antiname = 'ghWm~',
                spin = -1,
                color = 1,
                mass = Param.MW,
                width = Param.WW,
                texname = 'ghWm',
                antitexname = 'ghWm~',
                charge = -1,
                BL = 0,
                GhostNumber = 1,
                LeptonNumber = 0,
                Y = 0)

ghWm__tilde__ = ghWm.anti()

ghG = Particle(pdg_code = 82,
               name = 'ghG',
               antiname = 'ghG~',
               spin = -1,
               color = 8,
               mass = Param.ZERO,
               width = Param.ZERO,
               texname = 'ghG',
               antitexname = 'ghG~',
               charge = 0,
               BL = 0,
               GhostNumber = 1,
               LeptonNumber = 0,
               Y = 0)

ghG__tilde__ = ghG.anti()

Zp = Particle(pdg_code = 9900032,
              name = 'Zp',
              antiname = 'Zp',
              spin = 3,
              color = 1,
              mass = Param.MZp,
              width = Param.WZp,
              texname = 'Zp',
              antitexname = 'Zp',
              charge = 0,
              BL = 0,
              GhostNumber = 0,
              LeptonNumber = 0,
              Y = 0)

ghZp = Particle(pdg_code = 9000005,
                name = 'ghZp',
                antiname = 'ghZp~',
                spin = -1,
                color = 1,
                mass = Param.MZp,
                width = Param.WZp,
                texname = 'ghZp',
                antitexname = 'ghZp~',
                charge = 0,
                BL = 0,
                GhostNumber = 1,
                LeptonNumber = 0,
                Y = 0)

ghZp__tilde__ = ghZp.anti()

n1 = Particle(pdg_code = 12,
              name = 'n1',
              antiname = 'n1',
              spin = 2,
              color = 1,
              mass = Param.MnL1,
              width = Param.ZERO,
              texname = 'n1',
              antitexname = 'n1',
              charge = 0,
              BL = 0,
              GhostNumber = 0,
              LeptonNumber = 0,
              Y = 0)

n2 = Particle(pdg_code = 14,
              name = 'n2',
              antiname = 'n2',
              spin = 2,
              color = 1,
              mass = Param.MnL2,
              width = Param.ZERO,
              texname = 'n2',
              antitexname = 'n2',
              charge = 0,
              BL = 0,
              GhostNumber = 0,
              LeptonNumber = 0,
              Y = 0)

n3 = Particle(pdg_code = 16,
              name = 'n3',
              antiname = 'n3',
              spin = 2,
              color = 1,
              mass = Param.MnL3,
              width = Param.ZERO,
              texname = 'n3',
              antitexname = 'n3',
              charge = 0,
              BL = 0,
              GhostNumber = 0,
              LeptonNumber = 0,
              Y = 0)

nH1 = Particle(pdg_code = 9910012,
               name = 'nH1',
               antiname = 'nH1',
               spin = 2,
               color = 1,
               mass = Param.MnH1,
               width = Param.WnH1,
               texname = 'nH1',
               antitexname = 'nH1',
               charge = 0,
               BL = 0,
               GhostNumber = 0,
               LeptonNumber = 0,
               Y = 0)

nH2 = Particle(pdg_code = 9910014,
               name = 'nH2',
               antiname = 'nH2',
               spin = 2,
               color = 1,
               mass = Param.MnH2,
               width = Param.WnH2,
               texname = 'nH2',
               antitexname = 'nH2',
               charge = 0,
               BL = 0,
               GhostNumber = 0,
               LeptonNumber = 0,
               Y = 0)

nH3 = Particle(pdg_code = 9910016,
               name = 'nH3',
               antiname = 'nH3',
               spin = 2,
               color = 1,
               mass = Param.MnH3,
               width = Param.WnH3,
               texname = 'nH3',
               antitexname = 'nH3',
               charge = 0,
               BL = 0,
               GhostNumber = 0,
               LeptonNumber = 0,
               Y = 0)

e__minus__ = Particle(pdg_code = 11,
                      name = 'e-',
                      antiname = 'e+',
                      spin = 2,
                      color = 1,
                      mass = Param.Me,
                      width = Param.ZERO,
                      texname = 'e-',
                      antitexname = 'e+',
                      charge = -1,
                      BL = 0,
                      GhostNumber = 0,
                      LeptonNumber = 1,
                      Y = 0)

e__plus__ = e__minus__.anti()

mu__minus__ = Particle(pdg_code = 13,
                       name = 'mu-',
                       antiname = 'mu+',
                       spin = 2,
                       color = 1,
                       mass = Param.MMU,
                       width = Param.ZERO,
                       texname = 'mu-',
                       antitexname = 'mu+',
                       charge = -1,
                       BL = 0,
                       GhostNumber = 0,
                       LeptonNumber = 1,
                       Y = 0)

mu__plus__ = mu__minus__.anti()

ta__minus__ = Particle(pdg_code = 15,
                       name = 'ta-',
                       antiname = 'ta+',
                       spin = 2,
                       color = 1,
                       mass = Param.MTA,
                       width = Param.ZERO,
                       texname = 'ta-',
                       antitexname = 'ta+',
                       charge = -1,
                       BL = 0,
                       GhostNumber = 0,
                       LeptonNumber = 1,
                       Y = 0)

ta__plus__ = ta__minus__.anti()

u = Particle(pdg_code = 2,
             name = 'u',
             antiname = 'u~',
             spin = 2,
             color = 3,
             mass = Param.MU,
             width = Param.ZERO,
             texname = 'u',
             antitexname = 'u~',
             charge = 2/3,
             BL = 0,
             GhostNumber = 0,
             LeptonNumber = 0,
             Y = 0)

u__tilde__ = u.anti()

c = Particle(pdg_code = 4,
             name = 'c',
             antiname = 'c~',
             spin = 2,
             color = 3,
             mass = Param.MC,
             width = Param.ZERO,
             texname = 'c',
             antitexname = 'c~',
             charge = 2/3,
             BL = 0,
             GhostNumber = 0,
             LeptonNumber = 0,
             Y = 0)

c__tilde__ = c.anti()

t = Particle(pdg_code = 6,
             name = 't',
             antiname = 't~',
             spin = 2,
             color = 3,
             mass = Param.MT,
             width = Param.WT,
             texname = 't',
             antitexname = 't~',
             charge = 2/3,
             BL = 0,
             GhostNumber = 0,
             LeptonNumber = 0,
             Y = 0)

t__tilde__ = t.anti()

d = Particle(pdg_code = 1,
             name = 'd',
             antiname = 'd~',
             spin = 2,
             color = 3,
             mass = Param.MD,
             width = Param.ZERO,
             texname = 'd',
             antitexname = 'd~',
             charge = -1/3,
             BL = 0,
             GhostNumber = 0,
             LeptonNumber = 0,
             Y = 0)

d__tilde__ = d.anti()

s = Particle(pdg_code = 3,
             name = 's',
             antiname = 's~',
             spin = 2,
             color = 3,
             mass = Param.MS,
             width = Param.ZERO,
             texname = 's',
             antitexname = 's~',
             charge = -1/3,
             BL = 0,
             GhostNumber = 0,
             LeptonNumber = 0,
             Y = 0)

s__tilde__ = s.anti()

b = Particle(pdg_code = 5,
             name = 'b',
             antiname = 'b~',
             spin = 2,
             color = 3,
             mass = Param.MB,
             width = Param.ZERO,
             texname = 'b',
             antitexname = 'b~',
             charge = -1/3,
             BL = 0,
             GhostNumber = 0,
             LeptonNumber = 0,
             Y = 0)

b__tilde__ = b.anti()

H1 = Particle(pdg_code = 9900025,
              name = 'H1',
              antiname = 'H1',
              spin = 1,
              color = 1,
              mass = Param.MH1,
              width = Param.WH1,
              texname = 'H1',
              antitexname = 'H1',
              charge = 0,
              BL = 0,
              GhostNumber = 0,
              LeptonNumber = 0,
              Y = 0)

G0 = Particle(pdg_code = 250,
              name = 'G0',
              antiname = 'G0',
              spin = 1,
              color = 1,
              mass = Param.MZ,
              width = Param.WZ,
              texname = 'G0',
              antitexname = 'G0',
              goldstone = True,
              charge = 0,
              BL = 0,
              GhostNumber = 0,
              LeptonNumber = 0,
              Y = 0)

G__plus__ = Particle(pdg_code = 251,
                     name = 'G+',
                     antiname = 'G-',
                     spin = 1,
                     color = 1,
                     mass = Param.MW,
                     width = Param.WW,
                     texname = 'G+',
                     antitexname = 'G-',
                     goldstone = True,
                     charge = 1,
                     BL = 0,
                     GhostNumber = 0,
                     LeptonNumber = 0,
                     Y = 0)

G__minus__ = G__plus__.anti()

H2 = Particle(pdg_code = 9900026,
              name = 'H2',
              antiname = 'H2',
              spin = 1,
              color = 1,
              mass = Param.MH2,
              width = Param.WH2,
              texname = 'H2',
              antitexname = 'H2',
              charge = 0,
              BL = 0,
              GhostNumber = 0,
              LeptonNumber = 0,
              Y = 0)

phi0p = Particle(pdg_code = 9900252,
                 name = 'phi0p',
                 antiname = 'phi0p',
                 spin = 1,
                 color = 1,
                 mass = Param.MZp,
                 width = Param.ZERO,
                 texname = 'phi0p',
                 antitexname = 'phi0p',
                 goldstone = True,
                 charge = 0,
                 BL = 0,
                 GhostNumber = 0,
                 LeptonNumber = 0,
                 Y = 0)

