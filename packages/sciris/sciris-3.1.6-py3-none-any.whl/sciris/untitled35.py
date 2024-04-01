import numpy as np
import sciris as sc
import starsim as ss

import cProfile
import pstats


class cprofile(sc.prettyobj):
    def __init__(self, sort='cumtime', columns='default', mintime=1e-3, show=True, stripdirs=True):
        self.mintime = mintime
        self.show = show
        self.stripdirs = stripdirs
        self.sort = sort
        self.columns = columns
        self.parsed = None
        self.df = None
        self.profile = cProfile.Profile()
        return
    
    def parse_stats(self):
        if self.parsed is None:
            self.parsed = pstats.Stats(self.profile)
            if self.stripdirs:
                self.parsed = self.parsed.strip_dirs()
            self.n_functions = len(self.parsed.stats)
            self.total = self.parsed.total_tt
        return
    
    def to_df(self, sort=None, mintime=None, columns=None):
        """
        Parse data into a dataframe
        
        Column options are: 'default' (regular columns), 'brief' (only essential),
        or 'full' (all columns)
        """
        sort    = sc.ifelse(sort, self.sort)
        mintime = sc.ifelse(mintime, self.mintime)
        columns = sc.ifelse(columns, self.columns)
        
        # Settings
        cols = dict(
            brief = ['func', 'cumtime', 'selftime'],
            default = ['func', 'cumpct', 'selfpct', 'cumtime', 'selftime', 'calls', 'path'],
            full = ['calls', 'percall', 'selftime', 'cumtime', 'selfpct', 'cumpct', 'func', 'file', 'line'],
        )
        cols = cols[columns]
        
        # Parse the stats
        self.parse_stats()
        d = sc.dictobj()
        for key in ['calls', 'selftime', 'cumtime', 'file', 'line', 'func']:
            d[key] = []
        for key,entry in self.parsed.stats.items():
            _, ecall, eself, ecum, _ = entry
            if ecum >= mintime:
                efile,eline,efunc = key
                d.calls.append(ecall)
                d.selftime.append(eself)
                d.cumtime.append(ecum)
                d.file.append(efile)
                d.line.append(eline)
                d.func.append(efunc)
                
        # Convert to arrays
        for key in ['calls', 'selftime', 'cumtime']:
            d[key] = np.array(d[key])
        
        # Calculate additional columns
        d.percall = d.cumtime/d.calls
        d.cumpct  = d.cumtime/self.total*100
        d.selfpct = d.selftime/self.total*100
        d.path = []
        for fi,ln in zip(d.file, d.line):
            entry = fi if ln==0 else f'{fi}:{ln}'
            d.path.append(entry)
        
        # Convert to a dataframe
        data = {key:d[key] for key in cols}
        self.df = sc.dataframe(**data)
        reverse = sc.isarray(d[sort]) # If numeric, assume we want the highest first
        self.df = self.df.sortrows(sort, reverse=reverse)
        return self.df  
        
    def disp(self, *args, **kwargs):
        if self.df is None or args or kwargs:
            self.to_df(*args, **kwargs)
        self.df.disp()
        print(f'Total time: {self.total:n} s')
        if len(self.df) < self.n_functions:
            print(f'Note: {self.n_functions-len(self.df)} functions with time < {self.mintime} not shown.')
        return
    
    def enable(self):
        return self.profile.enable()
    
    def disable(self):
        return self.profile.disable()
    
    def __enter__(self):
        self.enable()
        return self
    
    def __exit__(self, *exc_info):
        self.disable()
        return

def big():
    for i in range(3):
        np.random.rand(int(1e8))

# with cprofile(sort='selfpct') as cpr:
#     sim = ss.demo(n_agents=100e3, run=True, plot=False)

cpr = cprofile(sort='selfpct')
cpr.enable()
sim = ss.demo(n_agents=100e3, run=True, plot=False)
cpr.disable()


cpr.disp()




# ps.print_stats()