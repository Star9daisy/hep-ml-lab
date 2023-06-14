# This file was automatically created by FeynRules 2.3.24
# Mathematica version: 12.0.0 for Mac OS X x86 (64-bit) (April 7, 2019)
# Date: Wed 9 Jun 2021 22:04:10


from object_library import all_vertices, Vertex
import particles as P
import couplings as C
import lorentz as L


V_1 = Vertex(name = 'V_1',
             particles = [ P.G0, P.G0, P.G0, P.G0 ],
             color = [ '1' ],
             lorentz = [ L.SSSS1 ],
             couplings = {(0,0):C.GC_56})

V_2 = Vertex(name = 'V_2',
             particles = [ P.G0, P.G0, P.G__minus__, P.G__plus__ ],
             color = [ '1' ],
             lorentz = [ L.SSSS1 ],
             couplings = {(0,0):C.GC_54})

V_3 = Vertex(name = 'V_3',
             particles = [ P.G__minus__, P.G__minus__, P.G__plus__, P.G__plus__ ],
             color = [ '1' ],
             lorentz = [ L.SSSS1 ],
             couplings = {(0,0):C.GC_55})

V_4 = Vertex(name = 'V_4',
             particles = [ P.G0, P.G0, P.H1, P.H1 ],
             color = [ '1' ],
             lorentz = [ L.SSSS1 ],
             couplings = {(0,0):C.GC_70})

V_5 = Vertex(name = 'V_5',
             particles = [ P.G__minus__, P.G__plus__, P.H1, P.H1 ],
             color = [ '1' ],
             lorentz = [ L.SSSS1 ],
             couplings = {(0,0):C.GC_70})

V_6 = Vertex(name = 'V_6',
             particles = [ P.H1, P.H1, P.H1, P.H1 ],
             color = [ '1' ],
             lorentz = [ L.SSSS1 ],
             couplings = {(0,0):C.GC_75})

V_7 = Vertex(name = 'V_7',
             particles = [ P.H2, P.H2, P.H2, P.H2 ],
             color = [ '1' ],
             lorentz = [ L.SSSS1 ],
             couplings = {(0,0):C.GC_74})

V_8 = Vertex(name = 'V_8',
             particles = [ P.G0, P.G0, P.H2, P.H2 ],
             color = [ '1' ],
             lorentz = [ L.SSSS1 ],
             couplings = {(0,0):C.GC_68})

V_9 = Vertex(name = 'V_9',
             particles = [ P.G__minus__, P.G__plus__, P.H2, P.H2 ],
             color = [ '1' ],
             lorentz = [ L.SSSS1 ],
             couplings = {(0,0):C.GC_68})

V_10 = Vertex(name = 'V_10',
              particles = [ P.H1, P.H1, P.H2, P.H2 ],
              color = [ '1' ],
              lorentz = [ L.SSSS1 ],
              couplings = {(0,0):C.GC_76})

V_11 = Vertex(name = 'V_11',
              particles = [ P.H2, P.H2, P.phi0p, P.phi0p ],
              color = [ '1' ],
              lorentz = [ L.SSSS1 ],
              couplings = {(0,0):C.GC_71})

V_12 = Vertex(name = 'V_12',
              particles = [ P.G0, P.G0, P.phi0p, P.phi0p ],
              color = [ '1' ],
              lorentz = [ L.SSSS1 ],
              couplings = {(0,0):C.GC_58})

V_13 = Vertex(name = 'V_13',
              particles = [ P.G__minus__, P.G__plus__, P.phi0p, P.phi0p ],
              color = [ '1' ],
              lorentz = [ L.SSSS1 ],
              couplings = {(0,0):C.GC_58})

V_14 = Vertex(name = 'V_14',
              particles = [ P.H1, P.H1, P.phi0p, P.phi0p ],
              color = [ '1' ],
              lorentz = [ L.SSSS1 ],
              couplings = {(0,0):C.GC_69})

V_15 = Vertex(name = 'V_15',
              particles = [ P.phi0p, P.phi0p, P.phi0p, P.phi0p ],
              color = [ '1' ],
              lorentz = [ L.SSSS1 ],
              couplings = {(0,0):C.GC_57})

V_16 = Vertex(name = 'V_16',
              particles = [ P.G0, P.G0, P.H1, P.H2 ],
              color = [ '1' ],
              lorentz = [ L.SSSS1 ],
              couplings = {(0,0):C.GC_67})

V_17 = Vertex(name = 'V_17',
              particles = [ P.G__minus__, P.G__plus__, P.H1, P.H2 ],
              color = [ '1' ],
              lorentz = [ L.SSSS1 ],
              couplings = {(0,0):C.GC_67})

V_18 = Vertex(name = 'V_18',
              particles = [ P.H1, P.H1, P.H1, P.H2 ],
              color = [ '1' ],
              lorentz = [ L.SSSS1 ],
              couplings = {(0,0):C.GC_72})

V_19 = Vertex(name = 'V_19',
              particles = [ P.H1, P.H2, P.H2, P.H2 ],
              color = [ '1' ],
              lorentz = [ L.SSSS1 ],
              couplings = {(0,0):C.GC_73})

V_20 = Vertex(name = 'V_20',
              particles = [ P.H1, P.H2, P.phi0p, P.phi0p ],
              color = [ '1' ],
              lorentz = [ L.SSSS1 ],
              couplings = {(0,0):C.GC_66})

V_21 = Vertex(name = 'V_21',
              particles = [ P.G0, P.G0, P.H1 ],
              color = [ '1' ],
              lorentz = [ L.SSS1 ],
              couplings = {(0,0):C.GC_165})

V_22 = Vertex(name = 'V_22',
              particles = [ P.G__minus__, P.G__plus__, P.H1 ],
              color = [ '1' ],
              lorentz = [ L.SSS1 ],
              couplings = {(0,0):C.GC_165})

V_23 = Vertex(name = 'V_23',
              particles = [ P.H1, P.H1, P.H1 ],
              color = [ '1' ],
              lorentz = [ L.SSS1 ],
              couplings = {(0,0):C.GC_168})

V_24 = Vertex(name = 'V_24',
              particles = [ P.H1, P.H2, P.H2 ],
              color = [ '1' ],
              lorentz = [ L.SSS1 ],
              couplings = {(0,0):C.GC_169})

V_25 = Vertex(name = 'V_25',
              particles = [ P.H1, P.phi0p, P.phi0p ],
              color = [ '1' ],
              lorentz = [ L.SSS1 ],
              couplings = {(0,0):C.GC_164})

V_26 = Vertex(name = 'V_26',
              particles = [ P.G0, P.G0, P.H2 ],
              color = [ '1' ],
              lorentz = [ L.SSS1 ],
              couplings = {(0,0):C.GC_163})

V_27 = Vertex(name = 'V_27',
              particles = [ P.G__minus__, P.G__plus__, P.H2 ],
              color = [ '1' ],
              lorentz = [ L.SSS1 ],
              couplings = {(0,0):C.GC_163})

V_28 = Vertex(name = 'V_28',
              particles = [ P.H1, P.H1, P.H2 ],
              color = [ '1' ],
              lorentz = [ L.SSS1 ],
              couplings = {(0,0):C.GC_166})

V_29 = Vertex(name = 'V_29',
              particles = [ P.H2, P.H2, P.H2 ],
              color = [ '1' ],
              lorentz = [ L.SSS1 ],
              couplings = {(0,0):C.GC_167})

V_30 = Vertex(name = 'V_30',
              particles = [ P.H2, P.phi0p, P.phi0p ],
              color = [ '1' ],
              lorentz = [ L.SSS1 ],
              couplings = {(0,0):C.GC_162})

V_31 = Vertex(name = 'V_31',
              particles = [ P.a, P.a, P.G__minus__, P.G__plus__ ],
              color = [ '1' ],
              lorentz = [ L.VVSS1 ],
              couplings = {(0,0):C.GC_6})

V_32 = Vertex(name = 'V_32',
              particles = [ P.a, P.G__minus__, P.G__plus__ ],
              color = [ '1' ],
              lorentz = [ L.VSS1 ],
              couplings = {(0,0):C.GC_3})

V_33 = Vertex(name = 'V_33',
              particles = [ P.ghA, P.ghWm__tilde__, P.W__minus__ ],
              color = [ '1' ],
              lorentz = [ L.UUV1 ],
              couplings = {(0,0):C.GC_3})

V_34 = Vertex(name = 'V_34',
              particles = [ P.ghA, P.ghWp__tilde__, P.W__plus__ ],
              color = [ '1' ],
              lorentz = [ L.UUV1 ],
              couplings = {(0,0):C.GC_4})

V_35 = Vertex(name = 'V_35',
              particles = [ P.ghWm, P.ghA__tilde__, P.G__plus__ ],
              color = [ '1' ],
              lorentz = [ L.UUS1 ],
              couplings = {(0,0):C.GC_151})

V_36 = Vertex(name = 'V_36',
              particles = [ P.ghWm, P.ghA__tilde__, P.W__plus__ ],
              color = [ '1' ],
              lorentz = [ L.UUV1 ],
              couplings = {(0,0):C.GC_3})

V_37 = Vertex(name = 'V_37',
              particles = [ P.ghWm, P.ghWm__tilde__, P.G0 ],
              color = [ '1' ],
              lorentz = [ L.UUS1 ],
              couplings = {(0,0):C.GC_144})

V_38 = Vertex(name = 'V_38',
              particles = [ P.ghWm, P.ghWm__tilde__, P.H1 ],
              color = [ '1' ],
              lorentz = [ L.UUS1 ],
              couplings = {(0,0):C.GC_146})

V_39 = Vertex(name = 'V_39',
              particles = [ P.ghWm, P.ghWm__tilde__, P.H2 ],
              color = [ '1' ],
              lorentz = [ L.UUS1 ],
              couplings = {(0,0):C.GC_148})

V_40 = Vertex(name = 'V_40',
              particles = [ P.ghWm, P.ghWm__tilde__, P.a ],
              color = [ '1' ],
              lorentz = [ L.UUV1 ],
              couplings = {(0,0):C.GC_4})

V_41 = Vertex(name = 'V_41',
              particles = [ P.ghWm, P.ghWm__tilde__, P.Z ],
              color = [ '1' ],
              lorentz = [ L.UUV1 ],
              couplings = {(0,0):C.GC_108})

V_42 = Vertex(name = 'V_42',
              particles = [ P.ghWm, P.ghZ__tilde__, P.G__plus__ ],
              color = [ '1' ],
              lorentz = [ L.UUS1 ],
              couplings = {(0,0):C.GC_154})

V_43 = Vertex(name = 'V_43',
              particles = [ P.ghWm, P.ghZ__tilde__, P.W__plus__ ],
              color = [ '1' ],
              lorentz = [ L.UUV1 ],
              couplings = {(0,0):C.GC_107})

V_44 = Vertex(name = 'V_44',
              particles = [ P.ghWp, P.ghA__tilde__, P.G__minus__ ],
              color = [ '1' ],
              lorentz = [ L.UUS1 ],
              couplings = {(0,0):C.GC_150})

V_45 = Vertex(name = 'V_45',
              particles = [ P.ghWp, P.ghA__tilde__, P.W__minus__ ],
              color = [ '1' ],
              lorentz = [ L.UUV1 ],
              couplings = {(0,0):C.GC_4})

V_46 = Vertex(name = 'V_46',
              particles = [ P.ghWp, P.ghWp__tilde__, P.G0 ],
              color = [ '1' ],
              lorentz = [ L.UUS1 ],
              couplings = {(0,0):C.GC_145})

V_47 = Vertex(name = 'V_47',
              particles = [ P.ghWp, P.ghWp__tilde__, P.H1 ],
              color = [ '1' ],
              lorentz = [ L.UUS1 ],
              couplings = {(0,0):C.GC_146})

V_48 = Vertex(name = 'V_48',
              particles = [ P.ghWp, P.ghWp__tilde__, P.H2 ],
              color = [ '1' ],
              lorentz = [ L.UUS1 ],
              couplings = {(0,0):C.GC_148})

V_49 = Vertex(name = 'V_49',
              particles = [ P.ghWp, P.ghWp__tilde__, P.a ],
              color = [ '1' ],
              lorentz = [ L.UUV1 ],
              couplings = {(0,0):C.GC_3})

V_50 = Vertex(name = 'V_50',
              particles = [ P.ghWp, P.ghWp__tilde__, P.Z ],
              color = [ '1' ],
              lorentz = [ L.UUV1 ],
              couplings = {(0,0):C.GC_107})

V_51 = Vertex(name = 'V_51',
              particles = [ P.ghWp, P.ghZ__tilde__, P.G__minus__ ],
              color = [ '1' ],
              lorentz = [ L.UUS1 ],
              couplings = {(0,0):C.GC_153})

V_52 = Vertex(name = 'V_52',
              particles = [ P.ghWp, P.ghZ__tilde__, P.W__minus__ ],
              color = [ '1' ],
              lorentz = [ L.UUV1 ],
              couplings = {(0,0):C.GC_108})

V_53 = Vertex(name = 'V_53',
              particles = [ P.ghZ, P.ghWm__tilde__, P.G__minus__ ],
              color = [ '1' ],
              lorentz = [ L.UUS1 ],
              couplings = {(0,0):C.GC_155})

V_54 = Vertex(name = 'V_54',
              particles = [ P.ghZ, P.ghWm__tilde__, P.W__minus__ ],
              color = [ '1' ],
              lorentz = [ L.UUV1 ],
              couplings = {(0,0):C.GC_107})

V_55 = Vertex(name = 'V_55',
              particles = [ P.ghZ, P.ghWp__tilde__, P.G__plus__ ],
              color = [ '1' ],
              lorentz = [ L.UUS1 ],
              couplings = {(0,0):C.GC_152})

V_56 = Vertex(name = 'V_56',
              particles = [ P.ghZ, P.ghWp__tilde__, P.W__plus__ ],
              color = [ '1' ],
              lorentz = [ L.UUV1 ],
              couplings = {(0,0):C.GC_108})

V_57 = Vertex(name = 'V_57',
              particles = [ P.ghZ, P.ghZ__tilde__, P.H1 ],
              color = [ '1' ],
              lorentz = [ L.UUS1 ],
              couplings = {(0,0):C.GC_156})

V_58 = Vertex(name = 'V_58',
              particles = [ P.ghZ, P.ghZ__tilde__, P.H2 ],
              color = [ '1' ],
              lorentz = [ L.UUS1 ],
              couplings = {(0,0):C.GC_158})

V_59 = Vertex(name = 'V_59',
              particles = [ P.ghZp, P.ghZp__tilde__, P.H2 ],
              color = [ '1' ],
              lorentz = [ L.UUS1 ],
              couplings = {(0,0):C.GC_59})

V_60 = Vertex(name = 'V_60',
              particles = [ P.ghZp, P.ghZp__tilde__, P.H1 ],
              color = [ '1' ],
              lorentz = [ L.UUS1 ],
              couplings = {(0,0):C.GC_64})

V_61 = Vertex(name = 'V_61',
              particles = [ P.ghG, P.ghG__tilde__, P.g ],
              color = [ 'f(1,2,3)' ],
              lorentz = [ L.UUV1 ],
              couplings = {(0,0):C.GC_10})

V_62 = Vertex(name = 'V_62',
              particles = [ P.g, P.g, P.g ],
              color = [ 'f(1,2,3)' ],
              lorentz = [ L.VVV1 ],
              couplings = {(0,0):C.GC_10})

V_63 = Vertex(name = 'V_63',
              particles = [ P.g, P.g, P.g, P.g ],
              color = [ 'f(-1,1,2)*f(3,4,-1)', 'f(-1,1,3)*f(2,4,-1)', 'f(-1,1,4)*f(2,3,-1)' ],
              lorentz = [ L.VVVV1, L.VVVV3, L.VVVV4 ],
              couplings = {(1,1):C.GC_12,(0,0):C.GC_12,(2,2):C.GC_12})

V_64 = Vertex(name = 'V_64',
              particles = [ P.u__tilde__, P.d, P.G__plus__ ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFS3, L.FFS5 ],
              couplings = {(0,0):C.GC_18,(0,1):C.GC_27})

V_65 = Vertex(name = 'V_65',
              particles = [ P.c__tilde__, P.d, P.G__plus__ ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFS3, L.FFS5 ],
              couplings = {(0,0):C.GC_19,(0,1):C.GC_28})

V_66 = Vertex(name = 'V_66',
              particles = [ P.t__tilde__, P.d, P.G__plus__ ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFS3, L.FFS5 ],
              couplings = {(0,0):C.GC_20,(0,1):C.GC_29})

V_67 = Vertex(name = 'V_67',
              particles = [ P.u__tilde__, P.s, P.G__plus__ ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFS3, L.FFS5 ],
              couplings = {(0,0):C.GC_21,(0,1):C.GC_30})

V_68 = Vertex(name = 'V_68',
              particles = [ P.c__tilde__, P.s, P.G__plus__ ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFS3, L.FFS5 ],
              couplings = {(0,0):C.GC_22,(0,1):C.GC_31})

V_69 = Vertex(name = 'V_69',
              particles = [ P.t__tilde__, P.s, P.G__plus__ ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFS3, L.FFS5 ],
              couplings = {(0,0):C.GC_23,(0,1):C.GC_32})

V_70 = Vertex(name = 'V_70',
              particles = [ P.u__tilde__, P.b, P.G__plus__ ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFS3, L.FFS5 ],
              couplings = {(0,0):C.GC_24,(0,1):C.GC_33})

V_71 = Vertex(name = 'V_71',
              particles = [ P.c__tilde__, P.b, P.G__plus__ ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFS3, L.FFS5 ],
              couplings = {(0,0):C.GC_25,(0,1):C.GC_34})

V_72 = Vertex(name = 'V_72',
              particles = [ P.t__tilde__, P.b, P.G__plus__ ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFS3, L.FFS5 ],
              couplings = {(0,0):C.GC_26,(0,1):C.GC_35})

V_73 = Vertex(name = 'V_73',
              particles = [ P.d__tilde__, P.d, P.G0 ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFS4 ],
              couplings = {(0,0):C.GC_176})

V_74 = Vertex(name = 'V_74',
              particles = [ P.s__tilde__, P.s, P.G0 ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFS4 ],
              couplings = {(0,0):C.GC_241})

V_75 = Vertex(name = 'V_75',
              particles = [ P.b__tilde__, P.b, P.G0 ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFS4 ],
              couplings = {(0,0):C.GC_170})

V_76 = Vertex(name = 'V_76',
              particles = [ P.d__tilde__, P.d, P.H1 ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFS6 ],
              couplings = {(0,0):C.GC_177})

V_77 = Vertex(name = 'V_77',
              particles = [ P.s__tilde__, P.s, P.H1 ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFS6 ],
              couplings = {(0,0):C.GC_242})

V_78 = Vertex(name = 'V_78',
              particles = [ P.b__tilde__, P.b, P.H1 ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFS6 ],
              couplings = {(0,0):C.GC_171})

V_79 = Vertex(name = 'V_79',
              particles = [ P.d__tilde__, P.d, P.H2 ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFS6 ],
              couplings = {(0,0):C.GC_178})

V_80 = Vertex(name = 'V_80',
              particles = [ P.s__tilde__, P.s, P.H2 ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFS6 ],
              couplings = {(0,0):C.GC_243})

V_81 = Vertex(name = 'V_81',
              particles = [ P.b__tilde__, P.b, P.H2 ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFS6 ],
              couplings = {(0,0):C.GC_172})

V_82 = Vertex(name = 'V_82',
              particles = [ P.n1, P.e__minus__, P.G__plus__ ],
              color = [ '1' ],
              lorentz = [ L.FFS3, L.FFS5 ],
              couplings = {(0,0):C.GC_182,(0,1):C.GC_195})

V_83 = Vertex(name = 'V_83',
              particles = [ P.n2, P.mu__minus__, P.G__plus__ ],
              color = [ '1' ],
              lorentz = [ L.FFS3, L.FFS5 ],
              couplings = {(0,0):C.GC_189,(0,1):C.GC_202})

V_84 = Vertex(name = 'V_84',
              particles = [ P.n3, P.ta__minus__, P.G__plus__ ],
              color = [ '1' ],
              lorentz = [ L.FFS3, L.FFS5 ],
              couplings = {(0,0):C.GC_250,(0,1):C.GC_209})

V_85 = Vertex(name = 'V_85',
              particles = [ P.e__plus__, P.e__minus__, P.G0 ],
              color = [ '1' ],
              lorentz = [ L.FFS4 ],
              couplings = {(0,0):C.GC_179})

V_86 = Vertex(name = 'V_86',
              particles = [ P.mu__plus__, P.mu__minus__, P.G0 ],
              color = [ '1' ],
              lorentz = [ L.FFS4 ],
              couplings = {(0,0):C.GC_186})

V_87 = Vertex(name = 'V_87',
              particles = [ P.ta__plus__, P.ta__minus__, P.G0 ],
              color = [ '1' ],
              lorentz = [ L.FFS4 ],
              couplings = {(0,0):C.GC_247})

V_88 = Vertex(name = 'V_88',
              particles = [ P.e__plus__, P.e__minus__, P.H1 ],
              color = [ '1' ],
              lorentz = [ L.FFS6 ],
              couplings = {(0,0):C.GC_180})

V_89 = Vertex(name = 'V_89',
              particles = [ P.mu__plus__, P.mu__minus__, P.H1 ],
              color = [ '1' ],
              lorentz = [ L.FFS6 ],
              couplings = {(0,0):C.GC_187})

V_90 = Vertex(name = 'V_90',
              particles = [ P.ta__plus__, P.ta__minus__, P.H1 ],
              color = [ '1' ],
              lorentz = [ L.FFS6 ],
              couplings = {(0,0):C.GC_248})

V_91 = Vertex(name = 'V_91',
              particles = [ P.e__plus__, P.e__minus__, P.H2 ],
              color = [ '1' ],
              lorentz = [ L.FFS6 ],
              couplings = {(0,0):C.GC_183})

V_92 = Vertex(name = 'V_92',
              particles = [ P.mu__plus__, P.mu__minus__, P.H2 ],
              color = [ '1' ],
              lorentz = [ L.FFS6 ],
              couplings = {(0,0):C.GC_190})

V_93 = Vertex(name = 'V_93',
              particles = [ P.ta__plus__, P.ta__minus__, P.H2 ],
              color = [ '1' ],
              lorentz = [ L.FFS6 ],
              couplings = {(0,0):C.GC_251})

V_94 = Vertex(name = 'V_94',
              particles = [ P.d__tilde__, P.u, P.G__minus__ ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFS3, L.FFS5 ],
              couplings = {(0,0):C.GC_36,(0,1):C.GC_45})

V_95 = Vertex(name = 'V_95',
              particles = [ P.s__tilde__, P.u, P.G__minus__ ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFS3, L.FFS5 ],
              couplings = {(0,0):C.GC_37,(0,1):C.GC_46})

V_96 = Vertex(name = 'V_96',
              particles = [ P.b__tilde__, P.u, P.G__minus__ ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFS3, L.FFS5 ],
              couplings = {(0,0):C.GC_38,(0,1):C.GC_47})

V_97 = Vertex(name = 'V_97',
              particles = [ P.d__tilde__, P.c, P.G__minus__ ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFS3, L.FFS5 ],
              couplings = {(0,0):C.GC_39,(0,1):C.GC_48})

V_98 = Vertex(name = 'V_98',
              particles = [ P.s__tilde__, P.c, P.G__minus__ ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFS3, L.FFS5 ],
              couplings = {(0,0):C.GC_40,(0,1):C.GC_49})

V_99 = Vertex(name = 'V_99',
              particles = [ P.b__tilde__, P.c, P.G__minus__ ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFS3, L.FFS5 ],
              couplings = {(0,0):C.GC_41,(0,1):C.GC_50})

V_100 = Vertex(name = 'V_100',
               particles = [ P.d__tilde__, P.t, P.G__minus__ ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFS3, L.FFS5 ],
               couplings = {(0,0):C.GC_42,(0,1):C.GC_51})

V_101 = Vertex(name = 'V_101',
               particles = [ P.s__tilde__, P.t, P.G__minus__ ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFS3, L.FFS5 ],
               couplings = {(0,0):C.GC_43,(0,1):C.GC_52})

V_102 = Vertex(name = 'V_102',
               particles = [ P.b__tilde__, P.t, P.G__minus__ ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFS3, L.FFS5 ],
               couplings = {(0,0):C.GC_44,(0,1):C.GC_53})

V_103 = Vertex(name = 'V_103',
               particles = [ P.u__tilde__, P.u, P.G0 ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFS4 ],
               couplings = {(0,0):C.GC_254})

V_104 = Vertex(name = 'V_104',
               particles = [ P.c__tilde__, P.c, P.G0 ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFS4 ],
               couplings = {(0,0):C.GC_173})

V_105 = Vertex(name = 'V_105',
               particles = [ P.t__tilde__, P.t, P.G0 ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFS4 ],
               couplings = {(0,0):C.GC_244})

V_106 = Vertex(name = 'V_106',
               particles = [ P.u__tilde__, P.u, P.H1 ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFS6 ],
               couplings = {(0,0):C.GC_255})

V_107 = Vertex(name = 'V_107',
               particles = [ P.c__tilde__, P.c, P.H1 ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFS6 ],
               couplings = {(0,0):C.GC_174})

V_108 = Vertex(name = 'V_108',
               particles = [ P.t__tilde__, P.t, P.H1 ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFS6 ],
               couplings = {(0,0):C.GC_245})

V_109 = Vertex(name = 'V_109',
               particles = [ P.u__tilde__, P.u, P.H2 ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFS6 ],
               couplings = {(0,0):C.GC_256})

V_110 = Vertex(name = 'V_110',
               particles = [ P.c__tilde__, P.c, P.H2 ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFS6 ],
               couplings = {(0,0):C.GC_175})

V_111 = Vertex(name = 'V_111',
               particles = [ P.t__tilde__, P.t, P.H2 ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFS6 ],
               couplings = {(0,0):C.GC_246})

V_112 = Vertex(name = 'V_112',
               particles = [ P.nH1, P.e__minus__, P.G__plus__ ],
               color = [ '1' ],
               lorentz = [ L.FFS3, L.FFS5 ],
               couplings = {(0,0):C.GC_184,(0,1):C.GC_193})

V_113 = Vertex(name = 'V_113',
               particles = [ P.nH2, P.mu__minus__, P.G__plus__ ],
               color = [ '1' ],
               lorentz = [ L.FFS3, L.FFS5 ],
               couplings = {(0,0):C.GC_191,(0,1):C.GC_200})

V_114 = Vertex(name = 'V_114',
               particles = [ P.nH3, P.ta__minus__, P.G__plus__ ],
               color = [ '1' ],
               lorentz = [ L.FFS3, L.FFS5 ],
               couplings = {(0,0):C.GC_252,(0,1):C.GC_207})

V_115 = Vertex(name = 'V_115',
               particles = [ P.a, P.W__minus__, P.G0, P.G__plus__ ],
               color = [ '1' ],
               lorentz = [ L.VVSS1 ],
               couplings = {(0,0):C.GC_109})

V_116 = Vertex(name = 'V_116',
               particles = [ P.a, P.W__minus__, P.G__plus__, P.H1 ],
               color = [ '1' ],
               lorentz = [ L.VVSS1 ],
               couplings = {(0,0):C.GC_110})

V_117 = Vertex(name = 'V_117',
               particles = [ P.a, P.W__minus__, P.G__plus__, P.H2 ],
               color = [ '1' ],
               lorentz = [ L.VVSS1 ],
               couplings = {(0,0):C.GC_114})

V_118 = Vertex(name = 'V_118',
               particles = [ P.a, P.W__minus__, P.G__plus__ ],
               color = [ '1' ],
               lorentz = [ L.VVS1 ],
               couplings = {(0,0):C.GC_150})

V_119 = Vertex(name = 'V_119',
               particles = [ P.W__minus__, P.G0, P.G__plus__ ],
               color = [ '1' ],
               lorentz = [ L.VSS1 ],
               couplings = {(0,0):C.GC_93})

V_120 = Vertex(name = 'V_120',
               particles = [ P.W__minus__, P.G__plus__, P.H1 ],
               color = [ '1' ],
               lorentz = [ L.VSS1 ],
               couplings = {(0,0):C.GC_94})

V_121 = Vertex(name = 'V_121',
               particles = [ P.W__minus__, P.G__plus__, P.H2 ],
               color = [ '1' ],
               lorentz = [ L.VSS1 ],
               couplings = {(0,0):C.GC_113})

V_122 = Vertex(name = 'V_122',
               particles = [ P.a, P.W__minus__, P.W__plus__ ],
               color = [ '1' ],
               lorentz = [ L.VVV1 ],
               couplings = {(0,0):C.GC_4})

V_123 = Vertex(name = 'V_123',
               particles = [ P.a, P.W__plus__, P.G0, P.G__minus__ ],
               color = [ '1' ],
               lorentz = [ L.VVSS1 ],
               couplings = {(0,0):C.GC_109})

V_124 = Vertex(name = 'V_124',
               particles = [ P.a, P.W__plus__, P.G__minus__, P.H1 ],
               color = [ '1' ],
               lorentz = [ L.VVSS1 ],
               couplings = {(0,0):C.GC_111})

V_125 = Vertex(name = 'V_125',
               particles = [ P.a, P.W__plus__, P.G__minus__, P.H2 ],
               color = [ '1' ],
               lorentz = [ L.VVSS1 ],
               couplings = {(0,0):C.GC_115})

V_126 = Vertex(name = 'V_126',
               particles = [ P.a, P.W__plus__, P.G__minus__ ],
               color = [ '1' ],
               lorentz = [ L.VVS1 ],
               couplings = {(0,0):C.GC_151})

V_127 = Vertex(name = 'V_127',
               particles = [ P.W__plus__, P.G0, P.G__minus__ ],
               color = [ '1' ],
               lorentz = [ L.VSS1 ],
               couplings = {(0,0):C.GC_92})

V_128 = Vertex(name = 'V_128',
               particles = [ P.W__plus__, P.G__minus__, P.H1 ],
               color = [ '1' ],
               lorentz = [ L.VSS1 ],
               couplings = {(0,0):C.GC_94})

V_129 = Vertex(name = 'V_129',
               particles = [ P.W__plus__, P.G__minus__, P.H2 ],
               color = [ '1' ],
               lorentz = [ L.VSS1 ],
               couplings = {(0,0):C.GC_113})

V_130 = Vertex(name = 'V_130',
               particles = [ P.W__minus__, P.W__plus__, P.G0, P.G0 ],
               color = [ '1' ],
               lorentz = [ L.VVSS1 ],
               couplings = {(0,0):C.GC_86})

V_131 = Vertex(name = 'V_131',
               particles = [ P.W__minus__, P.W__plus__, P.G__minus__, P.G__plus__ ],
               color = [ '1' ],
               lorentz = [ L.VVSS1 ],
               couplings = {(0,0):C.GC_86})

V_132 = Vertex(name = 'V_132',
               particles = [ P.W__minus__, P.W__plus__, P.H1, P.H1 ],
               color = [ '1' ],
               lorentz = [ L.VVSS1 ],
               couplings = {(0,0):C.GC_88})

V_133 = Vertex(name = 'V_133',
               particles = [ P.W__minus__, P.W__plus__, P.H1, P.H2 ],
               color = [ '1' ],
               lorentz = [ L.VVSS1 ],
               couplings = {(0,0):C.GC_90})

V_134 = Vertex(name = 'V_134',
               particles = [ P.W__minus__, P.W__plus__, P.H2, P.H2 ],
               color = [ '1' ],
               lorentz = [ L.VVSS1 ],
               couplings = {(0,0):C.GC_91})

V_135 = Vertex(name = 'V_135',
               particles = [ P.W__minus__, P.W__plus__, P.H1 ],
               color = [ '1' ],
               lorentz = [ L.VVS1 ],
               couplings = {(0,0):C.GC_147})

V_136 = Vertex(name = 'V_136',
               particles = [ P.W__minus__, P.W__plus__, P.H2 ],
               color = [ '1' ],
               lorentz = [ L.VVS1 ],
               couplings = {(0,0):C.GC_149})

V_137 = Vertex(name = 'V_137',
               particles = [ P.a, P.a, P.W__minus__, P.W__plus__ ],
               color = [ '1' ],
               lorentz = [ L.VVVV2 ],
               couplings = {(0,0):C.GC_5})

V_138 = Vertex(name = 'V_138',
               particles = [ P.W__minus__, P.W__plus__, P.Z ],
               color = [ '1' ],
               lorentz = [ L.VVV1 ],
               couplings = {(0,0):C.GC_108})

V_139 = Vertex(name = 'V_139',
               particles = [ P.W__minus__, P.W__minus__, P.W__plus__, P.W__plus__ ],
               color = [ '1' ],
               lorentz = [ L.VVVV2 ],
               couplings = {(0,0):C.GC_87})

V_140 = Vertex(name = 'V_140',
               particles = [ P.e__plus__, P.n1, P.G__minus__ ],
               color = [ '1' ],
               lorentz = [ L.FFS3, L.FFS5 ],
               couplings = {(0,0):C.GC_196,(0,1):C.GC_181})

V_141 = Vertex(name = 'V_141',
               particles = [ P.mu__plus__, P.n2, P.G__minus__ ],
               color = [ '1' ],
               lorentz = [ L.FFS3, L.FFS5 ],
               couplings = {(0,0):C.GC_203,(0,1):C.GC_188})

V_142 = Vertex(name = 'V_142',
               particles = [ P.ta__plus__, P.n3, P.G__minus__ ],
               color = [ '1' ],
               lorentz = [ L.FFS3, L.FFS5 ],
               couplings = {(0,0):C.GC_210,(0,1):C.GC_249})

V_143 = Vertex(name = 'V_143',
               particles = [ P.e__plus__, P.nH1, P.G__minus__ ],
               color = [ '1' ],
               lorentz = [ L.FFS3, L.FFS5 ],
               couplings = {(0,0):C.GC_194,(0,1):C.GC_185})

V_144 = Vertex(name = 'V_144',
               particles = [ P.mu__plus__, P.nH2, P.G__minus__ ],
               color = [ '1' ],
               lorentz = [ L.FFS3, L.FFS5 ],
               couplings = {(0,0):C.GC_201,(0,1):C.GC_192})

V_145 = Vertex(name = 'V_145',
               particles = [ P.ta__plus__, P.nH3, P.G__minus__ ],
               color = [ '1' ],
               lorentz = [ L.FFS3, L.FFS5 ],
               couplings = {(0,0):C.GC_208,(0,1):C.GC_253})

V_146 = Vertex(name = 'V_146',
               particles = [ P.n1, P.nH1, P.G0 ],
               color = [ '1' ],
               lorentz = [ L.FFS1 ],
               couplings = {(0,0):C.GC_199})

V_147 = Vertex(name = 'V_147',
               particles = [ P.n2, P.nH2, P.G0 ],
               color = [ '1' ],
               lorentz = [ L.FFS1 ],
               couplings = {(0,0):C.GC_206})

V_148 = Vertex(name = 'V_148',
               particles = [ P.n3, P.nH3, P.G0 ],
               color = [ '1' ],
               lorentz = [ L.FFS1 ],
               couplings = {(0,0):C.GC_213})

V_149 = Vertex(name = 'V_149',
               particles = [ P.n1, P.nH1, P.H1 ],
               color = [ '1' ],
               lorentz = [ L.FFS2 ],
               couplings = {(0,0):C.GC_220})

V_150 = Vertex(name = 'V_150',
               particles = [ P.n2, P.nH2, P.H1 ],
               color = [ '1' ],
               lorentz = [ L.FFS2 ],
               couplings = {(0,0):C.GC_229})

V_151 = Vertex(name = 'V_151',
               particles = [ P.n3, P.nH3, P.H1 ],
               color = [ '1' ],
               lorentz = [ L.FFS2 ],
               couplings = {(0,0):C.GC_238})

V_152 = Vertex(name = 'V_152',
               particles = [ P.n1, P.nH1, P.H2 ],
               color = [ '1' ],
               lorentz = [ L.FFS2 ],
               couplings = {(0,0):C.GC_219})

V_153 = Vertex(name = 'V_153',
               particles = [ P.n2, P.nH2, P.H2 ],
               color = [ '1' ],
               lorentz = [ L.FFS2 ],
               couplings = {(0,0):C.GC_228})

V_154 = Vertex(name = 'V_154',
               particles = [ P.n3, P.nH3, P.H2 ],
               color = [ '1' ],
               lorentz = [ L.FFS2 ],
               couplings = {(0,0):C.GC_237})

V_155 = Vertex(name = 'V_155',
               particles = [ P.nH1, P.nH1, P.G0 ],
               color = [ '1' ],
               lorentz = [ L.FFS1 ],
               couplings = {(0,0):C.GC_198})

V_156 = Vertex(name = 'V_156',
               particles = [ P.nH2, P.nH2, P.G0 ],
               color = [ '1' ],
               lorentz = [ L.FFS1 ],
               couplings = {(0,0):C.GC_205})

V_157 = Vertex(name = 'V_157',
               particles = [ P.nH3, P.nH3, P.G0 ],
               color = [ '1' ],
               lorentz = [ L.FFS1 ],
               couplings = {(0,0):C.GC_212})

V_158 = Vertex(name = 'V_158',
               particles = [ P.nH1, P.nH1, P.H1 ],
               color = [ '1' ],
               lorentz = [ L.FFS2 ],
               couplings = {(0,0):C.GC_218})

V_159 = Vertex(name = 'V_159',
               particles = [ P.nH2, P.nH2, P.H1 ],
               color = [ '1' ],
               lorentz = [ L.FFS2 ],
               couplings = {(0,0):C.GC_227})

V_160 = Vertex(name = 'V_160',
               particles = [ P.nH3, P.nH3, P.H1 ],
               color = [ '1' ],
               lorentz = [ L.FFS2 ],
               couplings = {(0,0):C.GC_236})

V_161 = Vertex(name = 'V_161',
               particles = [ P.nH1, P.nH1, P.H2 ],
               color = [ '1' ],
               lorentz = [ L.FFS2 ],
               couplings = {(0,0):C.GC_217})

V_162 = Vertex(name = 'V_162',
               particles = [ P.nH2, P.nH2, P.H2 ],
               color = [ '1' ],
               lorentz = [ L.FFS2 ],
               couplings = {(0,0):C.GC_226})

V_163 = Vertex(name = 'V_163',
               particles = [ P.nH3, P.nH3, P.H2 ],
               color = [ '1' ],
               lorentz = [ L.FFS2 ],
               couplings = {(0,0):C.GC_235})

V_164 = Vertex(name = 'V_164',
               particles = [ P.n1, P.n1, P.G0 ],
               color = [ '1' ],
               lorentz = [ L.FFS1 ],
               couplings = {(0,0):C.GC_197})

V_165 = Vertex(name = 'V_165',
               particles = [ P.n2, P.n2, P.G0 ],
               color = [ '1' ],
               lorentz = [ L.FFS1 ],
               couplings = {(0,0):C.GC_204})

V_166 = Vertex(name = 'V_166',
               particles = [ P.n3, P.n3, P.G0 ],
               color = [ '1' ],
               lorentz = [ L.FFS1 ],
               couplings = {(0,0):C.GC_211})

V_167 = Vertex(name = 'V_167',
               particles = [ P.n1, P.n1, P.H1 ],
               color = [ '1' ],
               lorentz = [ L.FFS2 ],
               couplings = {(0,0):C.GC_222})

V_168 = Vertex(name = 'V_168',
               particles = [ P.n2, P.n2, P.H1 ],
               color = [ '1' ],
               lorentz = [ L.FFS2 ],
               couplings = {(0,0):C.GC_231})

V_169 = Vertex(name = 'V_169',
               particles = [ P.n3, P.n3, P.H1 ],
               color = [ '1' ],
               lorentz = [ L.FFS2 ],
               couplings = {(0,0):C.GC_240})

V_170 = Vertex(name = 'V_170',
               particles = [ P.n1, P.n1, P.H2 ],
               color = [ '1' ],
               lorentz = [ L.FFS2 ],
               couplings = {(0,0):C.GC_221})

V_171 = Vertex(name = 'V_171',
               particles = [ P.n2, P.n2, P.H2 ],
               color = [ '1' ],
               lorentz = [ L.FFS2 ],
               couplings = {(0,0):C.GC_230})

V_172 = Vertex(name = 'V_172',
               particles = [ P.n3, P.n3, P.H2 ],
               color = [ '1' ],
               lorentz = [ L.FFS2 ],
               couplings = {(0,0):C.GC_239})

V_173 = Vertex(name = 'V_173',
               particles = [ P.nH1, P.nH1, P.phi0p ],
               color = [ '1' ],
               lorentz = [ L.FFS1 ],
               couplings = {(0,0):C.GC_214})

V_174 = Vertex(name = 'V_174',
               particles = [ P.nH2, P.nH2, P.phi0p ],
               color = [ '1' ],
               lorentz = [ L.FFS1 ],
               couplings = {(0,0):C.GC_223})

V_175 = Vertex(name = 'V_175',
               particles = [ P.nH3, P.nH3, P.phi0p ],
               color = [ '1' ],
               lorentz = [ L.FFS1 ],
               couplings = {(0,0):C.GC_232})

V_176 = Vertex(name = 'V_176',
               particles = [ P.n1, P.nH1, P.phi0p ],
               color = [ '1' ],
               lorentz = [ L.FFS1 ],
               couplings = {(0,0):C.GC_215})

V_177 = Vertex(name = 'V_177',
               particles = [ P.n2, P.nH2, P.phi0p ],
               color = [ '1' ],
               lorentz = [ L.FFS1 ],
               couplings = {(0,0):C.GC_224})

V_178 = Vertex(name = 'V_178',
               particles = [ P.n3, P.nH3, P.phi0p ],
               color = [ '1' ],
               lorentz = [ L.FFS1 ],
               couplings = {(0,0):C.GC_233})

V_179 = Vertex(name = 'V_179',
               particles = [ P.n1, P.n1, P.phi0p ],
               color = [ '1' ],
               lorentz = [ L.FFS1 ],
               couplings = {(0,0):C.GC_216})

V_180 = Vertex(name = 'V_180',
               particles = [ P.n2, P.n2, P.phi0p ],
               color = [ '1' ],
               lorentz = [ L.FFS1 ],
               couplings = {(0,0):C.GC_225})

V_181 = Vertex(name = 'V_181',
               particles = [ P.n3, P.n3, P.phi0p ],
               color = [ '1' ],
               lorentz = [ L.FFS1 ],
               couplings = {(0,0):C.GC_234})

V_182 = Vertex(name = 'V_182',
               particles = [ P.a, P.Z, P.G__minus__, P.G__plus__ ],
               color = [ '1' ],
               lorentz = [ L.VVSS1 ],
               couplings = {(0,0):C.GC_129})

V_183 = Vertex(name = 'V_183',
               particles = [ P.Z, P.G0, P.H1 ],
               color = [ '1' ],
               lorentz = [ L.VSS1 ],
               couplings = {(0,0):C.GC_125})

V_184 = Vertex(name = 'V_184',
               particles = [ P.Z, P.G0, P.H2 ],
               color = [ '1' ],
               lorentz = [ L.VSS1 ],
               couplings = {(0,0):C.GC_130})

V_185 = Vertex(name = 'V_185',
               particles = [ P.Z, P.G__minus__, P.G__plus__ ],
               color = [ '1' ],
               lorentz = [ L.VSS1 ],
               couplings = {(0,0):C.GC_124})

V_186 = Vertex(name = 'V_186',
               particles = [ P.W__minus__, P.Z, P.G0, P.G__plus__ ],
               color = [ '1' ],
               lorentz = [ L.VVSS1 ],
               couplings = {(0,0):C.GC_7})

V_187 = Vertex(name = 'V_187',
               particles = [ P.W__minus__, P.Z, P.G__plus__, P.H1 ],
               color = [ '1' ],
               lorentz = [ L.VVSS1 ],
               couplings = {(0,0):C.GC_9})

V_188 = Vertex(name = 'V_188',
               particles = [ P.W__minus__, P.Z, P.G__plus__, P.H2 ],
               color = [ '1' ],
               lorentz = [ L.VVSS1 ],
               couplings = {(0,0):C.GC_61})

V_189 = Vertex(name = 'V_189',
               particles = [ P.W__minus__, P.Z, P.G__plus__ ],
               color = [ '1' ],
               lorentz = [ L.VVS1 ],
               couplings = {(0,0):C.GC_143})

V_190 = Vertex(name = 'V_190',
               particles = [ P.W__plus__, P.Z, P.G0, P.G__minus__ ],
               color = [ '1' ],
               lorentz = [ L.VVSS1 ],
               couplings = {(0,0):C.GC_7})

V_191 = Vertex(name = 'V_191',
               particles = [ P.W__plus__, P.Z, P.G__minus__, P.H1 ],
               color = [ '1' ],
               lorentz = [ L.VVSS1 ],
               couplings = {(0,0):C.GC_8})

V_192 = Vertex(name = 'V_192',
               particles = [ P.W__plus__, P.Z, P.G__minus__, P.H2 ],
               color = [ '1' ],
               lorentz = [ L.VVSS1 ],
               couplings = {(0,0):C.GC_60})

V_193 = Vertex(name = 'V_193',
               particles = [ P.W__plus__, P.Z, P.G__minus__ ],
               color = [ '1' ],
               lorentz = [ L.VVS1 ],
               couplings = {(0,0):C.GC_142})

V_194 = Vertex(name = 'V_194',
               particles = [ P.a, P.W__minus__, P.W__plus__, P.Z ],
               color = [ '1' ],
               lorentz = [ L.VVVV5 ],
               couplings = {(0,0):C.GC_112})

V_195 = Vertex(name = 'V_195',
               particles = [ P.Z, P.Z, P.G0, P.G0 ],
               color = [ '1' ],
               lorentz = [ L.VVSS1 ],
               couplings = {(0,0):C.GC_138})

V_196 = Vertex(name = 'V_196',
               particles = [ P.Z, P.Z, P.G__minus__, P.G__plus__ ],
               color = [ '1' ],
               lorentz = [ L.VVSS1 ],
               couplings = {(0,0):C.GC_137})

V_197 = Vertex(name = 'V_197',
               particles = [ P.Z, P.Z, P.H1, P.H1 ],
               color = [ '1' ],
               lorentz = [ L.VVSS1 ],
               couplings = {(0,0):C.GC_139})

V_198 = Vertex(name = 'V_198',
               particles = [ P.Z, P.Z, P.H1, P.H2 ],
               color = [ '1' ],
               lorentz = [ L.VVSS1 ],
               couplings = {(0,0):C.GC_140})

V_199 = Vertex(name = 'V_199',
               particles = [ P.Z, P.Z, P.H2, P.H2 ],
               color = [ '1' ],
               lorentz = [ L.VVSS1 ],
               couplings = {(0,0):C.GC_141})

V_200 = Vertex(name = 'V_200',
               particles = [ P.Z, P.Z, P.H1 ],
               color = [ '1' ],
               lorentz = [ L.VVS1 ],
               couplings = {(0,0):C.GC_157})

V_201 = Vertex(name = 'V_201',
               particles = [ P.Z, P.Z, P.H2 ],
               color = [ '1' ],
               lorentz = [ L.VVS1 ],
               couplings = {(0,0):C.GC_159})

V_202 = Vertex(name = 'V_202',
               particles = [ P.W__minus__, P.W__plus__, P.Z, P.Z ],
               color = [ '1' ],
               lorentz = [ L.VVVV2 ],
               couplings = {(0,0):C.GC_89})

V_203 = Vertex(name = 'V_203',
               particles = [ P.Zp, P.H1, P.phi0p ],
               color = [ '1' ],
               lorentz = [ L.VSS1 ],
               couplings = {(0,0):C.GC_62})

V_204 = Vertex(name = 'V_204',
               particles = [ P.Zp, P.H2, P.phi0p ],
               color = [ '1' ],
               lorentz = [ L.VSS1 ],
               couplings = {(0,0):C.GC_15})

V_205 = Vertex(name = 'V_205',
               particles = [ P.Zp, P.Zp, P.H2, P.H2 ],
               color = [ '1' ],
               lorentz = [ L.VVSS1 ],
               couplings = {(0,0):C.GC_17})

V_206 = Vertex(name = 'V_206',
               particles = [ P.Zp, P.Zp, P.phi0p, P.phi0p ],
               color = [ '1' ],
               lorentz = [ L.VVSS1 ],
               couplings = {(0,0):C.GC_16})

V_207 = Vertex(name = 'V_207',
               particles = [ P.Zp, P.Zp, P.H1, P.H2 ],
               color = [ '1' ],
               lorentz = [ L.VVSS1 ],
               couplings = {(0,0):C.GC_63})

V_208 = Vertex(name = 'V_208',
               particles = [ P.Zp, P.Zp, P.H1, P.H1 ],
               color = [ '1' ],
               lorentz = [ L.VVSS1 ],
               couplings = {(0,0):C.GC_65})

V_209 = Vertex(name = 'V_209',
               particles = [ P.Zp, P.Zp, P.H2 ],
               color = [ '1' ],
               lorentz = [ L.VVS1 ],
               couplings = {(0,0):C.GC_160})

V_210 = Vertex(name = 'V_210',
               particles = [ P.Zp, P.Zp, P.H1 ],
               color = [ '1' ],
               lorentz = [ L.VVS1 ],
               couplings = {(0,0):C.GC_161})

V_211 = Vertex(name = 'V_211',
               particles = [ P.nH1, P.nH1, P.Zp ],
               color = [ '1' ],
               lorentz = [ L.FFV2 ],
               couplings = {(0,0):C.GC_79})

V_212 = Vertex(name = 'V_212',
               particles = [ P.nH2, P.nH2, P.Zp ],
               color = [ '1' ],
               lorentz = [ L.FFV2 ],
               couplings = {(0,0):C.GC_82})

V_213 = Vertex(name = 'V_213',
               particles = [ P.nH3, P.nH3, P.Zp ],
               color = [ '1' ],
               lorentz = [ L.FFV2 ],
               couplings = {(0,0):C.GC_85})

V_214 = Vertex(name = 'V_214',
               particles = [ P.n1, P.nH1, P.Zp ],
               color = [ '1' ],
               lorentz = [ L.FFV2 ],
               couplings = {(0,0):C.GC_77})

V_215 = Vertex(name = 'V_215',
               particles = [ P.n2, P.nH2, P.Zp ],
               color = [ '1' ],
               lorentz = [ L.FFV2 ],
               couplings = {(0,0):C.GC_80})

V_216 = Vertex(name = 'V_216',
               particles = [ P.n3, P.nH3, P.Zp ],
               color = [ '1' ],
               lorentz = [ L.FFV2 ],
               couplings = {(0,0):C.GC_83})

V_217 = Vertex(name = 'V_217',
               particles = [ P.n1, P.n1, P.Zp ],
               color = [ '1' ],
               lorentz = [ L.FFV2 ],
               couplings = {(0,0):C.GC_78})

V_218 = Vertex(name = 'V_218',
               particles = [ P.n2, P.n2, P.Zp ],
               color = [ '1' ],
               lorentz = [ L.FFV2 ],
               couplings = {(0,0):C.GC_81})

V_219 = Vertex(name = 'V_219',
               particles = [ P.n3, P.n3, P.Zp ],
               color = [ '1' ],
               lorentz = [ L.FFV2 ],
               couplings = {(0,0):C.GC_84})

V_220 = Vertex(name = 'V_220',
               particles = [ P.e__plus__, P.e__minus__, P.a ],
               color = [ '1' ],
               lorentz = [ L.FFV1 ],
               couplings = {(0,0):C.GC_3})

V_221 = Vertex(name = 'V_221',
               particles = [ P.mu__plus__, P.mu__minus__, P.a ],
               color = [ '1' ],
               lorentz = [ L.FFV1 ],
               couplings = {(0,0):C.GC_3})

V_222 = Vertex(name = 'V_222',
               particles = [ P.ta__plus__, P.ta__minus__, P.a ],
               color = [ '1' ],
               lorentz = [ L.FFV1 ],
               couplings = {(0,0):C.GC_3})

V_223 = Vertex(name = 'V_223',
               particles = [ P.u__tilde__, P.u, P.a ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV1 ],
               couplings = {(0,0):C.GC_2})

V_224 = Vertex(name = 'V_224',
               particles = [ P.c__tilde__, P.c, P.a ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV1 ],
               couplings = {(0,0):C.GC_2})

V_225 = Vertex(name = 'V_225',
               particles = [ P.t__tilde__, P.t, P.a ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV1 ],
               couplings = {(0,0):C.GC_2})

V_226 = Vertex(name = 'V_226',
               particles = [ P.d__tilde__, P.d, P.a ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV1 ],
               couplings = {(0,0):C.GC_1})

V_227 = Vertex(name = 'V_227',
               particles = [ P.s__tilde__, P.s, P.a ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV1 ],
               couplings = {(0,0):C.GC_1})

V_228 = Vertex(name = 'V_228',
               particles = [ P.b__tilde__, P.b, P.a ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV1 ],
               couplings = {(0,0):C.GC_1})

V_229 = Vertex(name = 'V_229',
               particles = [ P.u__tilde__, P.u, P.g ],
               color = [ 'T(3,2,1)' ],
               lorentz = [ L.FFV1 ],
               couplings = {(0,0):C.GC_11})

V_230 = Vertex(name = 'V_230',
               particles = [ P.c__tilde__, P.c, P.g ],
               color = [ 'T(3,2,1)' ],
               lorentz = [ L.FFV1 ],
               couplings = {(0,0):C.GC_11})

V_231 = Vertex(name = 'V_231',
               particles = [ P.t__tilde__, P.t, P.g ],
               color = [ 'T(3,2,1)' ],
               lorentz = [ L.FFV1 ],
               couplings = {(0,0):C.GC_11})

V_232 = Vertex(name = 'V_232',
               particles = [ P.d__tilde__, P.d, P.g ],
               color = [ 'T(3,2,1)' ],
               lorentz = [ L.FFV1 ],
               couplings = {(0,0):C.GC_11})

V_233 = Vertex(name = 'V_233',
               particles = [ P.s__tilde__, P.s, P.g ],
               color = [ 'T(3,2,1)' ],
               lorentz = [ L.FFV1 ],
               couplings = {(0,0):C.GC_11})

V_234 = Vertex(name = 'V_234',
               particles = [ P.b__tilde__, P.b, P.g ],
               color = [ 'T(3,2,1)' ],
               lorentz = [ L.FFV1 ],
               couplings = {(0,0):C.GC_11})

V_235 = Vertex(name = 'V_235',
               particles = [ P.d__tilde__, P.u, P.W__minus__ ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV3 ],
               couplings = {(0,0):C.GC_98})

V_236 = Vertex(name = 'V_236',
               particles = [ P.s__tilde__, P.u, P.W__minus__ ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV3 ],
               couplings = {(0,0):C.GC_99})

V_237 = Vertex(name = 'V_237',
               particles = [ P.b__tilde__, P.u, P.W__minus__ ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV3 ],
               couplings = {(0,0):C.GC_100})

V_238 = Vertex(name = 'V_238',
               particles = [ P.d__tilde__, P.c, P.W__minus__ ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV3 ],
               couplings = {(0,0):C.GC_101})

V_239 = Vertex(name = 'V_239',
               particles = [ P.s__tilde__, P.c, P.W__minus__ ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV3 ],
               couplings = {(0,0):C.GC_102})

V_240 = Vertex(name = 'V_240',
               particles = [ P.b__tilde__, P.c, P.W__minus__ ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV3 ],
               couplings = {(0,0):C.GC_103})

V_241 = Vertex(name = 'V_241',
               particles = [ P.d__tilde__, P.t, P.W__minus__ ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV3 ],
               couplings = {(0,0):C.GC_104})

V_242 = Vertex(name = 'V_242',
               particles = [ P.s__tilde__, P.t, P.W__minus__ ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV3 ],
               couplings = {(0,0):C.GC_105})

V_243 = Vertex(name = 'V_243',
               particles = [ P.b__tilde__, P.t, P.W__minus__ ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV3 ],
               couplings = {(0,0):C.GC_106})

V_244 = Vertex(name = 'V_244',
               particles = [ P.u__tilde__, P.d, P.W__plus__ ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV3 ],
               couplings = {(0,0):C.GC_257})

V_245 = Vertex(name = 'V_245',
               particles = [ P.c__tilde__, P.d, P.W__plus__ ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV3 ],
               couplings = {(0,0):C.GC_260})

V_246 = Vertex(name = 'V_246',
               particles = [ P.t__tilde__, P.d, P.W__plus__ ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV3 ],
               couplings = {(0,0):C.GC_263})

V_247 = Vertex(name = 'V_247',
               particles = [ P.u__tilde__, P.s, P.W__plus__ ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV3 ],
               couplings = {(0,0):C.GC_258})

V_248 = Vertex(name = 'V_248',
               particles = [ P.c__tilde__, P.s, P.W__plus__ ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV3 ],
               couplings = {(0,0):C.GC_261})

V_249 = Vertex(name = 'V_249',
               particles = [ P.t__tilde__, P.s, P.W__plus__ ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV3 ],
               couplings = {(0,0):C.GC_264})

V_250 = Vertex(name = 'V_250',
               particles = [ P.u__tilde__, P.b, P.W__plus__ ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV3 ],
               couplings = {(0,0):C.GC_259})

V_251 = Vertex(name = 'V_251',
               particles = [ P.c__tilde__, P.b, P.W__plus__ ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV3 ],
               couplings = {(0,0):C.GC_262})

V_252 = Vertex(name = 'V_252',
               particles = [ P.t__tilde__, P.b, P.W__plus__ ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV3 ],
               couplings = {(0,0):C.GC_265})

V_253 = Vertex(name = 'V_253',
               particles = [ P.e__plus__, P.n1, P.W__minus__ ],
               color = [ '1' ],
               lorentz = [ L.FFV3 ],
               couplings = {(0,0):C.GC_95})

V_254 = Vertex(name = 'V_254',
               particles = [ P.mu__plus__, P.n2, P.W__minus__ ],
               color = [ '1' ],
               lorentz = [ L.FFV3 ],
               couplings = {(0,0):C.GC_96})

V_255 = Vertex(name = 'V_255',
               particles = [ P.ta__plus__, P.n3, P.W__minus__ ],
               color = [ '1' ],
               lorentz = [ L.FFV3 ],
               couplings = {(0,0):C.GC_97})

V_256 = Vertex(name = 'V_256',
               particles = [ P.e__plus__, P.nH1, P.W__minus__ ],
               color = [ '1' ],
               lorentz = [ L.FFV3 ],
               couplings = {(0,0):C.GC_116})

V_257 = Vertex(name = 'V_257',
               particles = [ P.mu__plus__, P.nH2, P.W__minus__ ],
               color = [ '1' ],
               lorentz = [ L.FFV3 ],
               couplings = {(0,0):C.GC_117})

V_258 = Vertex(name = 'V_258',
               particles = [ P.ta__plus__, P.nH3, P.W__minus__ ],
               color = [ '1' ],
               lorentz = [ L.FFV3 ],
               couplings = {(0,0):C.GC_118})

V_259 = Vertex(name = 'V_259',
               particles = [ P.n1, P.e__minus__, P.W__plus__ ],
               color = [ '1' ],
               lorentz = [ L.FFV3 ],
               couplings = {(0,0):C.GC_95})

V_260 = Vertex(name = 'V_260',
               particles = [ P.n2, P.mu__minus__, P.W__plus__ ],
               color = [ '1' ],
               lorentz = [ L.FFV3 ],
               couplings = {(0,0):C.GC_96})

V_261 = Vertex(name = 'V_261',
               particles = [ P.n3, P.ta__minus__, P.W__plus__ ],
               color = [ '1' ],
               lorentz = [ L.FFV3 ],
               couplings = {(0,0):C.GC_97})

V_262 = Vertex(name = 'V_262',
               particles = [ P.nH1, P.e__minus__, P.W__plus__ ],
               color = [ '1' ],
               lorentz = [ L.FFV3 ],
               couplings = {(0,0):C.GC_116})

V_263 = Vertex(name = 'V_263',
               particles = [ P.nH2, P.mu__minus__, P.W__plus__ ],
               color = [ '1' ],
               lorentz = [ L.FFV3 ],
               couplings = {(0,0):C.GC_117})

V_264 = Vertex(name = 'V_264',
               particles = [ P.nH3, P.ta__minus__, P.W__plus__ ],
               color = [ '1' ],
               lorentz = [ L.FFV3 ],
               couplings = {(0,0):C.GC_118})

V_265 = Vertex(name = 'V_265',
               particles = [ P.u__tilde__, P.u, P.Z ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV3, L.FFV4 ],
               couplings = {(0,0):C.GC_123,(0,1):C.GC_120})

V_266 = Vertex(name = 'V_266',
               particles = [ P.c__tilde__, P.c, P.Z ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV3, L.FFV4 ],
               couplings = {(0,0):C.GC_123,(0,1):C.GC_120})

V_267 = Vertex(name = 'V_267',
               particles = [ P.t__tilde__, P.t, P.Z ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV3, L.FFV4 ],
               couplings = {(0,0):C.GC_123,(0,1):C.GC_120})

V_268 = Vertex(name = 'V_268',
               particles = [ P.d__tilde__, P.d, P.Z ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV3, L.FFV4 ],
               couplings = {(0,0):C.GC_122,(0,1):C.GC_119})

V_269 = Vertex(name = 'V_269',
               particles = [ P.s__tilde__, P.s, P.Z ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV3, L.FFV4 ],
               couplings = {(0,0):C.GC_122,(0,1):C.GC_119})

V_270 = Vertex(name = 'V_270',
               particles = [ P.b__tilde__, P.b, P.Z ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV3, L.FFV4 ],
               couplings = {(0,0):C.GC_122,(0,1):C.GC_119})

V_271 = Vertex(name = 'V_271',
               particles = [ P.n1, P.n1, P.Z ],
               color = [ '1' ],
               lorentz = [ L.FFV2 ],
               couplings = {(0,0):C.GC_126})

V_272 = Vertex(name = 'V_272',
               particles = [ P.n2, P.n2, P.Z ],
               color = [ '1' ],
               lorentz = [ L.FFV2 ],
               couplings = {(0,0):C.GC_127})

V_273 = Vertex(name = 'V_273',
               particles = [ P.n3, P.n3, P.Z ],
               color = [ '1' ],
               lorentz = [ L.FFV2 ],
               couplings = {(0,0):C.GC_128})

V_274 = Vertex(name = 'V_274',
               particles = [ P.n1, P.nH1, P.Z ],
               color = [ '1' ],
               lorentz = [ L.FFV2 ],
               couplings = {(0,0):C.GC_131})

V_275 = Vertex(name = 'V_275',
               particles = [ P.n2, P.nH2, P.Z ],
               color = [ '1' ],
               lorentz = [ L.FFV2 ],
               couplings = {(0,0):C.GC_133})

V_276 = Vertex(name = 'V_276',
               particles = [ P.n3, P.nH3, P.Z ],
               color = [ '1' ],
               lorentz = [ L.FFV2 ],
               couplings = {(0,0):C.GC_135})

V_277 = Vertex(name = 'V_277',
               particles = [ P.nH1, P.nH1, P.Z ],
               color = [ '1' ],
               lorentz = [ L.FFV2 ],
               couplings = {(0,0):C.GC_132})

V_278 = Vertex(name = 'V_278',
               particles = [ P.nH2, P.nH2, P.Z ],
               color = [ '1' ],
               lorentz = [ L.FFV2 ],
               couplings = {(0,0):C.GC_134})

V_279 = Vertex(name = 'V_279',
               particles = [ P.nH3, P.nH3, P.Z ],
               color = [ '1' ],
               lorentz = [ L.FFV2 ],
               couplings = {(0,0):C.GC_136})

V_280 = Vertex(name = 'V_280',
               particles = [ P.e__plus__, P.e__minus__, P.Z ],
               color = [ '1' ],
               lorentz = [ L.FFV3, L.FFV4 ],
               couplings = {(0,0):C.GC_124,(0,1):C.GC_121})

V_281 = Vertex(name = 'V_281',
               particles = [ P.mu__plus__, P.mu__minus__, P.Z ],
               color = [ '1' ],
               lorentz = [ L.FFV3, L.FFV4 ],
               couplings = {(0,0):C.GC_124,(0,1):C.GC_121})

V_282 = Vertex(name = 'V_282',
               particles = [ P.ta__plus__, P.ta__minus__, P.Z ],
               color = [ '1' ],
               lorentz = [ L.FFV3, L.FFV4 ],
               couplings = {(0,0):C.GC_124,(0,1):C.GC_121})

V_283 = Vertex(name = 'V_283',
               particles = [ P.e__plus__, P.e__minus__, P.Zp ],
               color = [ '1' ],
               lorentz = [ L.FFV1 ],
               couplings = {(0,0):C.GC_14})

V_284 = Vertex(name = 'V_284',
               particles = [ P.mu__plus__, P.mu__minus__, P.Zp ],
               color = [ '1' ],
               lorentz = [ L.FFV1 ],
               couplings = {(0,0):C.GC_14})

V_285 = Vertex(name = 'V_285',
               particles = [ P.ta__plus__, P.ta__minus__, P.Zp ],
               color = [ '1' ],
               lorentz = [ L.FFV1 ],
               couplings = {(0,0):C.GC_14})

V_286 = Vertex(name = 'V_286',
               particles = [ P.u__tilde__, P.u, P.Zp ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV1 ],
               couplings = {(0,0):C.GC_13})

V_287 = Vertex(name = 'V_287',
               particles = [ P.c__tilde__, P.c, P.Zp ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV1 ],
               couplings = {(0,0):C.GC_13})

V_288 = Vertex(name = 'V_288',
               particles = [ P.t__tilde__, P.t, P.Zp ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV1 ],
               couplings = {(0,0):C.GC_13})

V_289 = Vertex(name = 'V_289',
               particles = [ P.d__tilde__, P.d, P.Zp ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV1 ],
               couplings = {(0,0):C.GC_13})

V_290 = Vertex(name = 'V_290',
               particles = [ P.s__tilde__, P.s, P.Zp ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV1 ],
               couplings = {(0,0):C.GC_13})

V_291 = Vertex(name = 'V_291',
               particles = [ P.b__tilde__, P.b, P.Zp ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV1 ],
               couplings = {(0,0):C.GC_13})

