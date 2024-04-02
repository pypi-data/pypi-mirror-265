# Copyright (C) 2021-2024 Porte Verte

# =================================================================================================================================
# COMPANY SUFFIXES DICTIONARY AND LIST
# =================================================================================================================================

# dictionary to standardise names -- which will then be converted to a 2 dimensional list (with the key cascaded)

COMPANY_SUFFIXES_DICT = {
    'group holding ltd': ['group holding ltd', 'group holdings ltd', 'group holding ltd.', 'group holdings ltd.', 'group holding l.t.d.', 'group holdings l.t.d.', 'group holding limited', 'group holdings limited']
    , 'group holding': ['group holding', 'group holdings', 'grp holding', 'grp holdings', 'grp. holding', 'grp. holdings']
    , '& co ltd': ['& co ltd','& co. ltd', '& company ltd', '& co ltd.','& co ltd.','& co ltd.', '& co ltd.','& co. ltd.', '& company ltd.', '& co l.t.d.','& co l.t.d.','& co l.t.d.'
                   , '& co l.t.d.','& c.o. l.t.d.', '& company l.t.d.', '& co limited','& co limited','& co limited', '& co limited','& co. limited', '& company limited']
    , '& co': ['& co','& co.', '& c.o.', '&co', '& company', 'and co','and co.','and company', '+ co', '+ co.', '+ c.o.', '+co']
    , 'assoc': ['assoc', 'assoc.' 'association', 'assoc.']
    , 'corp': ['corp', 'corp.', 'corporated', 'corporation', 'corps']
    , 'pllc': ['pllc', 'pllc.', 'p.l.l.c.', 'public limited liability company']
    , 'lllp': ['lllp', 'lllp.', 'l.l.l.p.', 'limited liability limited partnership']
    , 'ltd': ['ltd', 'ltd.', 'l.t.d.', 'limited', 'limited company', 'l.t.d', 'l t d ', 'l. t. d.', 'limited.']
    , 'plc': ['plc', 'plc.', 'p.l.c.', 'public limited company', 'p l c', ' p. l. c.', 'p.l.c']
    , 'llc': ['llc', 'llc.', 'l.l.c.', 'limitied liability company', 'l.l.c', 'l l c', 'l. l. c.']
    , 'llp': ['llp', 'llp.', 'l.l.p.', 'limited liability partnership', 'l l p', 'l. l. p.']
    , 'inc': ['inc','inc.','incorporated', 'i n c', 'i. n. c.']
    , 'gmbh & co kg': ['gmbh & co kg', 'gmbh & co. kg', 'gmbh & co.kg' ,'gmbh&co kg', 'gmbh and co. kg', 'gmbh and co.kg', 'gmbh and co kg', 'gmbh + co. kg'
                       ,'gmbh + co.kg', 'gmbh + co kg', 'gmbh co. kg', 'gmbh co.kg', 'gmbh co kg']
    , 'bv & co kg': ['bv & co kg', 'bv & co. kg', 'bv & co.kg', 'bv&co kg', 'bv and co. kg', 'bv and co.kg', 'bv and co kg', 'bv + co. kg', 'bv + co.kg','bv + co kg', 'bv co. kg', 'bv co.kg', 'bv co kg']
    , 'se & co kg': ['se & co kg','se & co. kg', 'se & co. k.g.', 'se & co. kg.', 's.e. & co. kg', 'se & co kg.', 'se & co k.g.', 's.e. & co kg.', 'se and co kg', 'se and co. kg', 'se and co kg.', 'se and co k.g.', 's.e. and co kg', 'se. and co kg']
    , 'ag & co kg': ['ag & co kg','ag & co. kg', 'ag & co. k.g.', 'ag & co. kg.', 'a.g. & co. kg', 'ag & co kg.', 'ag & co k.g.', 'a.g. & co kg.', 'ag and co kg', 'ag and co. kg', 'ag and co kg.', 'ag and co k.g.', 'a.g. and co kg', 'ag. and co kg']    
    , 'gmbh': ['gmbh', 'gmbh.', 'g.m.b.h.', 'ggmbh', 'g.m.b.h', 'g m b h', 'g. m. b. h.']
    , 'ohg': ['ohg', 'ohg.', 'o.h.g.', 'o.h.g', 'o h g', 'o. h. g.']
    , 'ev': ['ev', 'e.v.', 'ev.', 'e. v.', 'e.v']
    , 'ag': ['ag', 'a.g.', 'ag.', 'a.g', 'a. g.']
    , 'kg': ['kg', 'k.g.', 'kg.', 'k.g', 'k g', 'k. g.']
    , 'ek': ['ek', 'e.k.', 'ek.', 'e.k', 'e. k.', 'e k', 'e.kfm', 'ekfm', 'e.kfr', 'ekfr', 'e. k']         
    , 'sarl': ['sarl', 'sarl.', 's.a.r.l.', 's.a.r.l', 's.a r.l', 's a r l', 's. a. r. l.', 's.a r.l.']
    , 'sas': ['sas', 's.a.s.', 'sas.', 's.a.s', 's a s', 's. a. s.']
    , 'snc': ['snc', 'snc.', 's.n.c.', 's.n.c', 's n c', 's. n. c.']
    , 'sa': ['sa', 's.a.', 'sa.', 's.a', 'sa .', 's a', 's.a..', 's. a', 's. a .', 's . a .', 's. a.']
    , 'scarl': ['scarl', 's.c.a.r.l.', 's.c.a.r.l', 'scarl.']
    , 'scpa': ['scpa', 's.c.p.a.', 's.c.p.a', 'scpa.', 's c p a', 's. c. p. a.']
    , 'srl': ['srl', 'srl.', 's.r.l.', 's.r.l', 'srls', 'srls.', 's.r.l.s.', 's.r.l', 'sr.l.', 's.rl.', 's r l', 's. r. l.']
    , 'spa': ['spa', 's.p.a.', 'spa.', 's.pa', 'sp.a', 's.p.a', 's..p.a.', 's p a', 's. p. a.', 's p a', 's. p. a.']
    , 'bv': ['bv', 'b.v.', 'bv.', 'b.v', 'b v.', 'b. v', 'b. v.', 'b v', '.b.v']
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
    , 'coop v': ['coop v', 'coop. v.', 'coop. v', 'coop v.']
    , 'sccl': ['sccl', 's.c.c.l.', 's.c.c.l', 'sccl.', 's c c l ', 's. c. c. l.']
    , 'slu': ['slu', 's.l.u.', 'slu.', 's.l.u', 's l u', 's. l. u.']
    , 'slp': ['slp', 's.l.p.', 'slp.', 's. l. p.', 's.l.p', 's l p']
    , 'sau': ['sau', 's.a.u.', 'sau.', 's.a.u', 's a u', 's. a. u.']
    , 'sl': ['sl', 's.l.', 'sl.', 's l', 's.l', 's. l.']          
    , 'lda': ['lda', 'l.d.a.', 'lda.', 'l.d.a', 'limitada', 'l d a', 'l. d. a.']            
    , 'sc': ['sc', 's.c.', 'sc.', 's.c', 'sc .', 's c', 's. c', 's. c .', 's . c .']
    , 'aps': ['aps', 'a.p.s.', 'a.p.s', 'aps.', 'aps .', ' a p s', 'a. p. s.']
    , 'ab': ['ab', 'a.b.', 'a.b', 'a b', 'a. b.']        
    , 'spol sro': ['spol sro', 'spol. sro', 'spol.s r.o.', 'spol. s r', 'spol. s r.o.', 'spol. s.r.o.', 'spol. s r. o.', 'spol. s r.o', 'spol. s r.o'
                   , 'spol. s r. o.', 'spol. s .r.o.', 'spol. s r.o.', 'spol. s. r. o', 'spol. s. r. o.', 'spol. s.r.o', 'spol.s r.o', 'spol.r.o.', 'spol. s r. o']
    , 'sro': ['sro', 'sro.', 's.r.o.', 's r.o.', 's r.o', 's. r. o.','s r. o.', 's.r.o', 's. r. o', 's r o', 's r o.', 's.r. o', 's r.o', 's r. o.,', 's.r.o', 's .r.o.', 's.r.o']     
    , 'o.p.s.': ['o.p.s.', 'o.p.s', 'o. p. s.']
    , 'vos':['vos', 'vos.', 'v.o.s.', 'v.o.s']
    , 'as': ['as', 'a.s.','a. s.', 'a s.', 'a. s', 'a s', 'a.s.,', 'a.s. ,', 'a .s.', 'a.s', 'a..s.', 'as.', '.a.s']
    , 'ks':['ks', 'ks.', 'k.s.', 'k.s', 'k s', 'k. s.']
    , 'zs':['zs', 'zs.', 'z.s.', 'z.s', 'z s', 'z. s.']            
    , 'sp zoo spk': ['sp zoo spk', 'sp zoo sp k', 'sp. z.o.o. s.p. k.', 'sp. z.o.o. s.p.k.', 'sp. z o.o. sp. k','sp. z o.o sp.k.','sp. z o.o. sk',  'sp z o.o. sp.k.'
                     , 'sp. z o. o. sp. k.', 'sp. z o.o. sp.k.', 'sp. z o.o. sp. k.', 'sp z o.o. sp.k', 'sp. z.o.o. sp.k.', 'sp. z o.o. sp.k', 'sp. z o. o. sp. k'
                     , 'sp. z.o. sp. k', 'sp. z o.o. spk', 'sp.z o.o. sp.k', 'sp z o.o. sp. k.', 'sp. z o.o. sp. k.a', 'sp.z o.o. sp. k.']
    , 'sp zoo spj': ['sp zoo spj', 'sp. z.o.o. sp.j', 'sp. z.o.o. sp. j', 'sp. z.o.o. sp. j.', 'sp. z o.o. sp.j.', 'sp. z o.o. sp. j.', 'sp. z o. o. sp. j.']
    , 'sp zoo ska': ['sp zoo ska', 'sp. z.o.o. s.k.a.', 'sp. z o.o. s. k.a', 'sp. z o.o. s.k.a.',  'sp. z oo s.k.a.', 'sp. z o.o. s.k.', 'sp. z o.o. s.k.a', 'sp. z o. o. ska']
    , 'sp zoo': ['sp zoo', 'sp. z.o.o.', 'sp z o o',  'sp z o.o',  'sp z o.o.',  'sp. z o o',  'sp. z o. o.', 'sp. z o.o',  'sp. z o.o.',  'sp. z. o. o.', 'sp.z o.o', 'sp.z o.o.'
                 , 's.p. z.o.o.', 's.p. zoo', 'sp zoo.', 'sp. zoo', 'sp. zoo.', 'sp z oo', 'sp zo.o.', 'sp.z.o.o.', 'sp. z o. o', 'spo. z o.o.', 'sp. z o .o.', 'sp z o. o', 'sp z.o.o.']
    , 'spj': ['spj', 'sp j', 'sp. j', 'sp j.', 'sp.j', 'sp.j.', 'sp. j.']
    , 'spk': ['spk', 'sp k', 'sp. k', 'sp k.', 'sp.k', 'sp.k.', 'sp. k.']
    , 'ltd sti': ['ltd sti', 'ltd. sti.', 'l.t.d. s.t.i.', 'l t g s t i', 'l. t. d. s. t. i.', 'ltdsti', 'ltdsti.', 'l.t.d.s.t.i.', 'ltd. sti', 'ltd sti.', 'ltd.sti.', 'ltd.sti']
    , 'pjsc': ['pjsc', 'p.j.s.c.', 'pjsc.', 'p.j.s.c', 'public joint stock company', 'public joint-stock company']
    , 'ojsc': ['ojsc', 'o.j.s.c.', 'ojsc.', 'o.j.s.c']
    , 'cjsc': ['cjsc', 'c.j.s.c.', 'cjsc.', 'c.j.s.c']
    , 'jsc': ['jsc', 'j.s.c.', 'jsc.', 'j.s.c', 'joint stock company', 'joint-stock company']
    , 'ooo': ['ooo', 'o.o.o.', 'ooo.', 'o.o.o']
    , 'oao': ['oao', 'o.a.o.', 'oao.', 'o.a.o']
    , 'rao': ['rao', 'r.a.o.', 'rao.', 'r.a.o']
    , 'pao': ['pao', 'p.a.o.', 'pao.', 'p.a.o']            
    , 'doo': ['doo', 'd.o.o.', 'd.o.o', 'doo.', 'd.o.o. s.k.', 'd o o', 'd. o. o.']
    , 'wll': ['wll', 'w.l.l.', 'wll.', 'w.l.l', 'w. l. l.', 'w l l']
    , 'nyrt': ['nyrt', 'n.y.r.t.', 'n.y.r.t', 'nyrt.', 'n. y. r. t. ', 'n y r t']
    , 'kft': ['kft', 'kft.', 'k.f.t.', 'k.f.t', 'k. f. t.', 'k f t']
    , 'zrt': ['zrt', 'zrt.', 'z.r.t.', 'z.r.t', 'z. r. t.', 'z r t']
    , 'kkt': ['kkt', 'kkt.', 'k.k.t.', 'k.k.t', 'k. k. t.', 'k k t']
    , 'epe': ['epe', 'e.p.e.', 'e.p.e', 'epe.', 'e. p. e.', 'e p e ']
    , 'ae':['ae', 'ae.', 'a.e.', 'a.e', 'a e', 'a. e.']
    , 'oe':['oe', 'oe.', 'o.e.', 'o.e', 'o e', 'o. e.']
    , 'ee':['ee', 'ee.', 'e.e.', 'e.e', 'e e', 'e. e.']
    , 'se': ['se', 's.e.', 'se.', 's.e'] 
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