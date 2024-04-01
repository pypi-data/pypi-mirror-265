# Copyright (C) 2021-2024 Porte Verte

# =================================================================================================================================
# COMPANY SUFFIXES DICTIONARY AND LIST
# =================================================================================================================================

# dictionary to standardise names -- which will then be converted to a 2 dimensional list (with the key cascaded)
# each country section does not necessarily comprise all terms for that country -- just dictionary addenda

COMPANY_SUFFIXES_DICT = {
    # uk
    'group holding ltd': ['group holding ltd', 'group holdings ltd', 'group holding ltd.', 'group holdings ltd.', 'group holding l.t.d.', 'group holdings l.t.d.'
                          , 'group holding limited', 'group holdings limited']
    , 'group holding': ['group holding', 'group holdings', 'grp holding', 'grp holdings', 'grp. holding', 'grp. holdings']
    , '& co ltd': ['& co ltd','& co. ltd', '& company ltd', '& co ltd.','& co ltd.','& co ltd.', '& co ltd.','& co. ltd.', '& company ltd.', '& co l.t.d.'
                   ,'& co l.t.d.','& co l.t.d.', '& co l.t.d.','& c.o. l.t.d.', '& company l.t.d.', '& co limited','& co limited','& co limited', '& co limited'
                   ,'& co. limited', '& company limited']
    , '& co': ['& co','& co.', '& c.o.', '&co', '& company', 'and co','and co.','and company', '+ co', '+ co.', '+ c.o.', '+co']
    , 'assoc': ['assoc', 'assoc.' 'association', 'assoc.']
    , 'corp': ['corp', 'corp.', 'corporated', 'corporation', 'corps']
    , 'pllc': ['pllc', 'pllc.', 'p.l.l.c.', 'public limited liability company']
    , 'lllp': ['lllp', 'lllp.', 'l.l.l.p.', 'limited liability limited partnership']
    , 'ltd': ['ltd', 'ltd.', 'l.t.d.', 'limited', 'limited company', 'l.t.d', 'l t d ', 'l. t. d.', 'ltd. .', 'ltd. 2', 'ltd 2', 'limited.']
    , 'plc': ['plc', 'plc.', 'p.l.c.', 'public limited company', 'p l c', ' p. l. c.', 'p.l.c']
    , 'llc': ['llc', 'llc.', 'l.l.c.', 'limitied liability company', 'l.l.c', 'l l c', 'l. l. c.']
    , 'llp': ['llp', 'llp.', 'l.l.p.', 'limited liability partnership', 'l l p', 'l. l. p.']
    , 'inc': ['inc','inc.','incorporated', 'i n c', 'i. n. c.']
    # germany
    , 'gmbh & co kg': ['gmbh & co kg', 'gmbh & co. kg', 'gmbh & co.kg' ,'gmbh&co kg', 'gmbh and co. kg', 'gmbh and co.kg', 'gmbh and co kg', 'gmbh + co. kg'
                       ,'gmbh + co.kg', 'gmbh + co kg', 'gmbh co. kg', 'gmbh co.kg', 'gmbh co kg', 'gmbh 6co. kg', 'gmbh 6co.kg', 'gmbh 6co kg'
                       , 'gmbha &a co.a kg', 'gmbhcokg','gmbh kg', 'gmbh & co. k', 'gmbh und co. kg', 'gmbh und co.', 'gmbh& co.', 'gmbh & co. kgaa'
                       , 'gmbh & co kgaa','gmbh &co', 'gmbh+co.kg', 'gmbh & co .kg', 'mbh &co. kg', 'gmbh u. co.', 'gmbh &co.', 'gmbh&co.kg', 'gmbh u co'
                       , 'gmbh & c', 'gmbh &. co.kg', 'gmbh u. co', 'gmbh &. co', 'gmbh& co.kg', 'gmbh & co. og', 'gmbh & co.', '& co.gmbh & co.', 'mbh & co.kg'
                       , 'gmbh & co.kg.', 'gmbh & co', 'gesmbh & co kg', 'gmbh und co.kg', 'gmbh und co. kg', 'mbh & co. kg', 'gmbh u. co kg', 'gmbh u. co. kg'
                       , 'gmbh &. co kg', 'gmbh und co kg', 'gmbh and co k', 'gmbh&co. kg', 'gmbh u. co.kg', 'gmbh &co.kg', 'gmbh & co . kg', 'gesellschaft mbh & cokg'
                       , 'ges.m.b.h. & co kg', 'gesellschaft m.b.h. u. co. kg', 'gmbh & cco kg', 'ges.m.b.h & co. kg', 'gmbh & co. kg kg', 'gmbh & co kg i. gr.'
                       , 'gmbh & co. kg - 2017', 'gmbh & cokg', 'gmbh u co']
    , 'bv & co kg': ['bv & co kg', 'bv & co. kg', 'bv & co.kg', 'bv&co kg', 'bv and co. kg', 'bv and co.kg', 'bv and co kg', 'bv + co. kg', 'bv + co.kg',
                     'bv + co kg', 'bv co. kg', 'bv co.kg', 'bv co kg', 'bv 6co. kg', 'bv 6co.kg', 'bv 6co kg', 'bva &a co.a kg', 'bvcokg', 'b. v. & co. kg']
    , 'se & co kg': ['se & co kg','se & co. kg', 'se & co. k.g.', 'se & co. kg.', 's.e. & co. kg', 'se & co kg.', 'se & co k.g.', 's.e. & co kg.', 'se and co kg'
                     , 'se and co. kg', 'se and co kg.', 'se and co k.g.', 's.e. and co kg', 'se. and co kg', 'se & co. k']
    , 'ag & co kg': ['ag & co kg','ag & co. kg', 'ag & co. k.g.', 'ag & co. kg.', 'a.g. & co. kg', 'ag & co kg.', 'ag & co k.g.', 'a.g. & co kg.', 'ag and co kg'
                     , 'ag and co. kg', 'ag and co kg.', 'ag and co k.g.', 'a.g. and co kg', 'ag. and co kg', 'ag & co. k', 'ag&co kg', 'ag & co.kg']    
    , 'gmbh': ['gmbh', 'gmbh.', 'g.m.b.h.', 'ggmbh', 'g.m.b.h', 'g m b h', 'g. m. b. h.', 'g bh', 'ges.m.b.h.', 'gesellschaft mit beschrankter haftung', 'ges.m.b.h'
               , 'gesellschaft m.b.h', 'gesmbh.', 'gesellschaft m.b.h.', 'ges.m.h', 'gesellschaft m. b. h.', 'gesmb.h.', 'gesellschaft mbh', 'gmbh alt']
    , 'ohg': ['ohg', 'ohg.', 'o.h.g.', 'o.h.g', 'o h g', 'o. h. g.', 'offene handelsgesellschaft']
    , 'ev': ['ev', 'e.v.', 'ev.', 'e. v.', 'e.v. 2', 'e.v']
    , 'ag': ['ag', 'a.g.', 'ag.', 'a.g', 'aktiengesellschaft', 'a. g.']
    , 'kg': ['kg', 'k.g.', 'kg.', 'k.g', 'k g', 'k. g.', 'kommanditgesellschaft']
    , 'ek': ['ek', 'e.k.', 'ek.', 'e.k', 'e. k.', 'e k', 'e.kfm', 'ekfm', 'e.kfr', 'ekfr', 'eingetragener kaufmann', 'e. k']         
    # france
    , 'sarl': ['sarl', 'sarl.', 's.a.r.l.', 's.a.r.l', 's.a r.l', 's a r l', 's. a. r. l.', 's.a r.l.']
    , 'sas': ['sas', 's.a.s.', 'sas.', 's.a.s', 's a s', 's. a. s.', 'sas-2']
    , 'snc': ['snc', 'snc.', 's.n.c.', 's.n.c', 's n c', 's. n. c.']
    , 'sa': ['sa', 's.a.', 'sa.', 's.a', 'sa .', 's a', 's.a..', 's. a', 's. a .', 's . a .', 'sa 2', 's. a.', '- sa', 's.a. 2', 'sa - 2']
     # italy
    , 'scarl': ['scarl', 's.c.a.r.l.', 's.c.a.r.l', 'scarl.', 's.c. a r.l.']
    , 'scpa': ['scpa', 's.c.p.a.', 's.c.p.a', 'scpa.', 's c p a', 's. c. p. a.']
    , 'srl': ['srl', 'srl.', 's.r.l.', 's.r.l', 'srls', 'srls.', 's.r.l.s.', 's.r.l', 'sr.l.', 's.rl.', 's r l', 's. r. l.', 'srl 2', 's.r.l.u.', 's.r.l.s', 's.r l']
    , 'spa': ['spa', 's.p.a.', 'spa.', 's.pa', 'sp.a', 's.p.a', 's..p.a.', 's p a', 's. p. a.', 's p a', 's. p. a.', 'spa - 2']
    # netherlands
    , 'bv': ['bv', 'b.v.', 'bv.', 'b.v', 'b v.', 'b. v', 'b. v.', 'b v', '.b.v']
    # belgium
    , 'commv': ['commv', 'c.o.m.m.v.', 'c.o.m.m.v', 'commv.', 'comm.v.']
    , 'cvba': ['cvba', 'c.v.b.a.', 'c.v.b.a', 'cvba.']
    , 'bvba': ['bvba', 'b.v.b.a.', 'b.v.b.a', 'bvba.']
    , 'asbl': ['asbl', 'a.s.b.l.', 'a.s.b.l', 'asbl.']
    , 'scrl': ['scrl', 's.c.r.l.', 's.c.r.l', 'scrl.']
    , 'sprl': ['sprl', 's.p.r.l.', 's.p.r.l', 'sprl.']
    , 'ivzw': ['ivzw', 'i.v.z.w.', 'i.v.z.w', 'ivzw.']
    , 'vof': ['vof', 'v.o.f.', 'v.o.f', 'vof.']
    , 'vzw': ['vzw', 'v.z.w.', 'v.z.w', 'vzw.']
    , 'cv': ['cv', 'c.v.', 'cv.', 'c.v', 'c. v.']
    , 'nv': ['nv', 'n.v.', 'nv.', 'n.v', 'n. v.']
    # spain
    , 'coop v': ['coop v', 'coop. v.', 'coop. v', 'coop v.']
    , 'sccl': ['sccl', 's.c.c.l.', 's.c.c.l', 'sccl.', 's c c l ', 's. c. c. l.']
    , 'slu': ['slu', 's.l.u.', 'slu.', 's.l.u', 's l u', 's. l. u.']
    , 'slp': ['slp', 's.l.p.', 'slp.', 's. l. p.', 's.l.p', 's l p']
    , 'sau': ['sau', 's.a.u.', 'sau.', 's.a.u', 's a u', 's. a. u.']
    , 'sl': ['sl', 's.l.', 'sl.', 's l', 's.l', 's. l.']          
    # portugal
    , 'lda': ['lda', 'l.d.a.', 'lda.', 'l.d.a', 'limitada', 'l d a', 'l. d. a.']            
    , 'sc': ['sc', 's.c.', 'sc.', 's.c', 'sc .', 's c', 's.c..', 's. c', 's. c .', 's . c .', 's.c. 2']
    # denmark
    , 'aps': ['aps', 'a.p.s.', 'a.p.s', 'aps.', 'aps .', ' a p s', 'a. p. s.']
    # swdeden
    , 'ab': ['ab', 'a.b.', 'a.b', 'a b', 'a. b.', 'aktiebolag', 'a/b']
    # czech republic            
    , 'spol sro': ['spol sro', 'spol. sro', 'spol.s r.o.', 'spol. s r. o._2', 'spol. s r.o.,_2', 'spol. s r. o._2', 'spol. s r', 'spol. s r.o.', 'spol. s.r.o.'
                   , 'spol. s r. o.', 'spol. s r.o', 'spol. s r.o', 'spol. s r..o.', 'spol. s r. o.', 'spol. s .r.o.', 'spol. s r.o.', 'spol. s. r. o'
                   , 'spol. s. r. o.', 'spol. s.r.o', 'spol.s r.o', 'spol.r.o.', 'spol. s r. o']
    , 'sro': ['sro', 'sro.', 's.r.o.', 's r.o.', 's r.o', 's. r. o.','s r. o.', 's.r.o', 's .r.o.', 's.r.o.,', 's r..o.', 's.r.o.,,', 's. r. o', 's r o', 's r o.'
              , 's.r. o', 's r.o', 's r. o.,', 's.r.o', 's .r.o.', 's.r.o', 's.r.o.,', 's.r.o..', 's.r.o,', 's. r. o._2', 's r.o_2', 's r.o._2', 's.ro.'
              , 's.r.o._2', 's.r.o. 2', 's.r.o..', 's..r.o.', 's.r.o.2', 's.r.o .']     
    , 'o.p.s.': ['o.p.s.', 'o.p.s', 'o. p. s.']
    , 'vos':['vos', 'vos.', 'v.o.s.', 'v.o.s']
    , 'as': ['as', 'a.s.','a. s.', 'a s.', 'a. s', 'a s', 'a.s.,', 'a.s. ,', 'a .s.', 'a.s', 'a.s..', 'a.s.,.', 'a.s.,,', 'a.s._2', 'a.s._', 'a..s.', 'a.s...'
             , 'a..s.', 'as.', 'a/s', 'a/s.', 'a.s. 2', 'a / s', '.a.s', 'a.s. . .']
    , 'ks':['ks', 'ks.', 'k.s.', 'k.s', 'k s', 'k. s.']
    , 'zs':['zs', 'zs.', 'z.s.', 'z.s', 'z s', 'z. s.']            
    # poland
    , 'sp zoo spk': ['sp zoo spk', 'sp zoo sp k', 'sp. z.o.o. s.p. k.', 'sp. z.o.o. s.p.k.', 'sp. z o.o. sp. k','sp. z o.o sp.k.','sp. z o.o. sk',  'sp z o.o. sp.k.'
                     , 'sp. z o. o. sp. k.', 'sp. z o.o. sp.k.', 'sp. z o.o. sp. k.', 'sp z o.o. sp.k', 'sp. z.o.o. sp.k.', 'sp. z o.o. sp.k', 'sp. z o. o. sp. k'
                     , 'sp. z o.o. sp. kom.', 'sp. z.o. sp. k', 'sp. z o.o. spk', 'sp.z o.o. sp.k', 'sp z o.o. sp. k.', 'sp. z o.o. sp. k.a', 'spolka z o. o. sp. k'
                     , 'sp. z o. o. sp. kom.', 'sp.z o.o. sp. k.', 'sp. z o.o. spolka komandytowa', 'sp z o.o. spolka komandytowa', 'sp z o o spolka komandytowa'
                     , 'spolka z o.o. spolka komandytowa', 'sp. z o. o. spolka komandytowa', 'sp. z o.o. spolka komandytowa', 'sp. z.o.o. sp. k.', 'sp. z o.o. sp.'
                     , 'sp.zo.o. sp.k.', 'sp. zo.o. sp.k', 'sp. z.o.o. sp.k', 'spolka z ograniczona odpowiedzialnoscia sp.k', 'spolka z ograniczona odpowiedzialnoscia sp. k'
                     , 'spolka z ograniczona odpowiedzialnoscia sp k', 'spolka z ograniczona odpowiedzialnoscia spk', 'sp.z o.o. sp.k.', 'sp z.o.o sp. k', 'spolka zoo - sp.k.'
                     , 'spolka z ograniczona odpowiedzialnoscia sp.k. 1', 'sp zo.o sp. k.', 'spolka z ogran iczona odpowiedzialnoscia sp.k.'
                     , 'spolka z ograniczona odpowiedzialnoscia sp.k.', 'spolka z ograniczona odpowiedzialnoscia sp. k.', 'spolka z ograniczona odpowiedzialnoscia - sp.k.'
                     , 'spolka z o o. sp. k.', 'sp. z o.o sp.k', 'sp.zo.o sp.k', 'sp. z o. o. sp.k.', 'sp. zo.o. sp.k.', 'sp. zo.o. sp. komandytowa', 'spolka z o.o. sp.k.'
                     , 'sp z o.o. s.k.', 'sp z o o spolka k', 'sp.z o. o. sp. k.', 'sp. o. o. sp. k.', 'sp. z.o.o sp. kom.', 'sp.zo.o. s p. k.', 'sp.z o.o.sp.k'
                     , 'spolka z o.o. sp. k.', 'sp. z o.o. sp. komandytowa']
    , 'sp zoo spj': ['sp zoo spj', 'sp. z o.o. sp. jawna', 'sp. z o.o. spolka jawna', 'sp. z.o.o. sp.j', 'sp. z.o.o. sp. j', 'sp. z.o.o. sp. j.', 'sp. z o.o. sp.j.'
                     , 'sp. z o.o. - sp.j', 'sp. z o.o. sp. j.', 'sp. z o. o. sp. j.']
    , 'sp zoo ska': ['sp zoo ska', 'sp. z.o.o. s.k.a.', 'sp. z o.o. s. k.a', 'sp. z o.o. s.k.a.',  'sp. z oo s.k.a.', 'sp. z o.o. s.k.', 'sp. z o. o. s. k.'
                     , 'sp. z o.o. s.k.a', 'sp. z o. o. ska', 'sp. z o.o. 4f s.k.a.', 'spolka z ograniczona odpowiedzialnoscia s.k.a.'
                     , 'spolka z ograniczona odpowiedzialnoscia ska', 'spolka z ograniczona odpowiedzialnoscia ska.', 'spolka z o.o. s.k.a.', 'sp. z o.o. ska'
                     , 'sp. z o.o.s.k.a', 'sp. z o. o. s. k. a.', 'sp. z o.o.s.k.a.', 'sp. z o.o. s.kom']
    , 'sp zoo': ['sp zoo', 'sp. z.o.o.', 'sp z o o',  'sp z o.o',  'sp z o.o.',  'sp. z o o',  'sp. z o. o.', 'sp. z o.o',  'sp. z o.o.',  'sp. z. o. o.', 'sp.z o.o'
                 , 'sp.z o.o.', 's.p. z.o.o.', 's.p. zoo', 'sp zoo.', 'sp. zoo', 'sp. zoo.', 'sp z oo', 'sp zo.o.', 'sp.z.o.o.', 'sp. z o. o', 'spo. z o.o.', 'sp. z o .o.'
                 , 'sp z o. o', 'sp z.o.o.', 'spolka z o.o.', 'sp. zo.o.', 'sp. z .o.o.', 'sp. z o .o', 'sp. z o . o.', 'sp . sp zoo', 'sp. z.o.o', 'sp. z o', 'sp. z. o.o.'
                 , 'spolka z ograniczona odpowiedzialnoscia', 'sp. z o.o. 2', 'sp z o. o.', 'sp. z o.o. ul.', 'sp. z o.o. 3', 'sp. z o.o 1', 'sp. z .o.o', 'spolka z o. o.'
                 , 'spolka z o.o', 'sp.zo.o.', 'sp.zo.o', 'sp. zo. o.', 'sp.z o.', 'sp.z o', 'sp.z.o.o', 'spz o.o.', 'sp.z o. o.', 'sp. z o.o. 4', 'sp. z o.o 2'
                 , 'sp. z o.o._4', 'sp. z o.o._3', 'sp. z o.o._2', 'sp. z oo']
    , 'spj': ['spj', 'sp j', 'sp. j', 'sp j.', 'sp.j', 'sp.j.', 'spolka jawna', 'sp. j.', 'sp. jawna']
    , 'spk': ['spk', 'sp k', 'sp. k', 'sp k.', 'sp.k', 'sp.k.', 'spolka komandytowa', 'sp. k.']
    # Turkey
    , 'ltd sti': ['ltd sti', 'ltd. sti.', 'l.t.d. s.t.i.', 'l t g s t i', 'l. t. d. s. t. i.', 'ltdsti', 'ltdsti.', 'l.t.d.s.t.i.', 'ltd. sti', 'ltd sti.'
                  , 'ltd. sti..', 'ltd.. sti.', 'ltd.sti.', 'ltd.sti']
    , 'ao': ['ao', 'a.o.','a. o.', 'a o.', 'a. o', 'a o', 'a.o.,', 'a.o. ,', 'a .o.', 'a.o', 'a.o..', 'a.o.,.', 'a.o.,,', 'a.o._2', 'a.o._', 'a..o.', 'a/o'
             , 'a.o...', 'a..o.', 'ao.']
    # russia
    , 'pjsc': ['pjsc', 'p.j.s.c.', 'pjsc.', 'p.j.s.c', 'public joint stock company', 'public joint-stock company']
    , 'ojsc': ['ojsc', 'o.j.s.c.', 'ojsc.', 'o.j.s.c']
    , 'cjsc': ['cjsc', 'c.j.s.c.', 'cjsc.', 'c.j.s.c']
    , 'jsc': ['jsc', 'j.s.c.', 'jsc.', 'j.s.c', 'joint stock company', 'joint-stock company']
    , 'ooo': ['ooo', 'o.o.o.', 'ooo.', 'o.o.o']
    , 'oao': ['oao', 'o.a.o.', 'oao.', 'o.a.o']
    , 'rao': ['rao', 'r.a.o.', 'rao.', 'r.a.o']
    , 'pao': ['pao', 'p.a.o.', 'pao.', 'p.a.o']            
    # serbia
    , 'doo': ['doo', 'd.o.o.', 'd.o.o', 'doo.', 'd.o.o. s.k.', 'd o o', 'd. o. o.', 'd.o.o. 6','d.o.o. 1']
    # qatar
    , 'wll': ['wll', 'w.l.l.', 'wll.', 'w.l.l', 'w. l. l.', 'w l l']
    # hungary
    , 'nyrt': ['nyrt', 'n.y.r.t.', 'n.y.r.t', 'nyrt.', 'n. y. r. t. ', 'n y r t', 'nyilvanosan mukodo reszvenytarsasag']
    , 'kft': ['kft', 'kft.', 'k.f.t.', 'k.f.t', 'k. f. t.', 'k f t', 'korlatolt felelossegu tarsasag']
    , 'zrt': ['zrt', 'zrt.', 'z.r.t.', 'z.r.t', 'z. r. t.', 'z r t', 'zartkoruen mukodo reszvenytarsasag', 'zrt. 2']
    , 'kkt': ['kkt', 'kkt.', 'k.k.t.', 'k.k.t', 'k. k. t.', 'k k t', 'kozkereseti tarsasag']
    # greece
    , 'epe': ['epe', 'e.p.e.', 'e.p.e', 'epe.', 'e. p. e.', 'e p e ']
    , 'ae':['ae', 'ae.', 'a.e.', 'a.e', 'a e', 'a. e.']
    , 'oe':['oe', 'oe.', 'o.e.', 'o.e', 'o e', 'o. e.']
    , 'ee':['ee', 'ee.', 'e.e.', 'e.e', 'e e', 'e. e.']
    # europe
    , 'se': ['se', 's.e.', 'se.', 's.e'] 
    # others
    , 'vvi': ['vvi', 'v.v.i.', 'v. v. i.', 'v.v.i.,,', 'v.vi.'] 
    , 'z.u.': ['zu', 'z.u.', 'z. u.', 'z u.', 'z. u', 'z u']
}

# =================================================================================================================================
# =================================================================================================================================
# =================================================================================================================================

# =================================================================================================================================
# DOMAIN SUFFIXES LIST
# =================================================================================================================================

# list of domain suffixes to iteratively remove from domain (all items in the list will be removed from the end)
# so mydomain.com.fr woudl be stripped to mydomain as would mydomain.fr.com (but only .com and .fr need to be in the list)

DOMAIN_SUFFIXES_LIST = [
                    '.ac','.ac.uk','.ad','.ae','.aero','.af','.ag','.ai','.al','.am','.an','.ao','.aq','.ar','.arpa','.as','.asia','.at','.au','.aw'
                    ,'.ax','.az','.ba','.bb','.bd','.be','.bf','.bg','.bh','.bi','.biz','.bj','.bm','.bn','.bo','.br','.bs','.bt','.bv','.bw','.by'
                    ,'.bz','.ca','.cat','.cc','.cd','.cf','.cg','.ch','.ci','.ck','.cl','.cm','.cn','.co','.co.uk','.com','.coop','.cr','.cs','.cu'
                    ,'.cv','.cw','.cx','.cy','.cym.uk','.cz','.dd','.de','.dj','.dk','.dm','.do','.dz','.ec','.edu','.ee','.eg','.eh','.er','.es'
                    ,'.et','.eu','.fi','.firm','.fj','.fk','.fm','.fo','.fr','.fx','.ga','.gb','.gd','.ge','.gf','.gg','.gh','.gi','.gl','.gm','.gn'
                    ,'.gov','.gov.uk','.govt.uk','.gp','.gq','.gr','.gs','.gt','.gu','.gw','.gy','.hk','.hm','.hn','.hr','.ht','.hu','.id','.ie','.il'
                    ,'.im','.in','.info','.int','.io','.iq','.ir','.is','.it','.Itd.uk','.je','.jm','.jo','.jobs','.jp','.ke','.kg','.kh','.ki','.km'
                    ,'.kn','.kp','.kr','.kw','.ky','.kz','.la','.lb','.lc','.lea.uk','.li','.lk','.lr','.ls','.lt','.ltd.uk','.lu','.lv','.ly','.ma'
                    ,'.mc','.md','.me','.me.uk','.mg','.mh','.mil','.mil.uk','.mk','.ml','.mm','.mn','.mo','.mobi','.mod.uk','.mp','.mq','.mr','.ms'
                    ,'.mt','.mu','.museum','.mv','.mw','.mx','.my','.mz','.na','.name','.nato','.nc','.ne','.net','.net.uk','.nf','.ng','.nhs.uk','.ni'
                    ,'.nic.uk','.nl','.no','.nom','.np','.nr','.nt','.nu','.nz','.om','.org','.org.uk','.orgn.uk','.pa','.parliament.uk','.pe','.pf'
                    ,'.pg','.ph','.pic.uk','.pk','.pl','.plc.uk','.pm','.pn','.post','.pr','.pro','.ps','.pt','.pw','.py','.qa','.re','.ro','.rs','.ru'
                    ,'.rw','.sa','.sb','.sc','.sch.uk','.scot.uk','.sd','.se','.sg','.sh','.si','.sj','.sk','.sl','.sm','.sn','.so','.soc.uk','.sr'
                    ,'.ss','.st','.store','.su','.sv','.sy','.sz','.tc','.td','.tel','.tf','.tg','.th','.tj','.tk','.tl','.tm','.tn','.to','.tp','.tr'
                    ,'.travel','.tt','.tv','.tw','.tz','.ua','.ug','.uk','.um','.us','.uy','.uz','.va','.vc','.ve','.vg','.vi','.vn','.vu','.web','.wf'
                    ,'.ws','.xxx','.ye','.yt','.yu','.za','.zm','.zr','.zw','.eus'
]

# =================================================================================================================================
# =================================================================================================================================
# =================================================================================================================================