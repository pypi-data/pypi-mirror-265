from dreamcreator.sequences.core.smu_sweep import SmuSweep

class VoltageSweepIda(SmuSweep):
    """
    Voltage sweep sequence class.

    Args:
        ps (Dreams Lab probe station object): the probe station performing the sweep.
    """
    def __init__(self, ps):
        self.variables = {
            'Start': 0, 
            'Start_info': 'Please enter start voltage (V)',
            'Stop': 1, 
            'Stop_info': 'Please enter stop voltage (V)',
            'Res': 100, 
            'Res_info': 'Please enter stepsize (mV)',
            'IV': 'True',
            'IV_info': 'Enter True to receive IV plot',
            'RV': 'True',
            'RV_info': 'Enter True to receive RV plot',
            'PV': 'True',
            'PV_info': 'Enter True to receive PV plot',
            'Channel A': 'True',
            'Channel A_info': 'Please enter True to use Channel A if not enter False',
            'Channel B': 'False',
            'Channel B_info': 'Please enter True to use Channel B if not enter False'
        }

        self.resultsinfo = {
            'num_plots': 1,
            'visual': True,
            'saveplot': True,
            'plottitle': 'Voltage Sweep',
            'save_location': '',
            'foldername': '',
            'xtitle': 'Voltage (V)',
            'ytitle': 'Current (A)',
            'xscale': 1,
            'yscale': 1,
            'legend': True,
            'csv': True,
            'pdf': True,
            'mat': True,
            'pkl': True
        }
        
        super().__init__(variables=self.variables,sweeptype='voltage', resultsinfo=self.resultsinfo, ps=ps)

        

    def run(self,routine=False):
        self.set_results(variables=self.variables, resultsinfo = self.resultsinfo, routine=routine)
        settings = self.ps.get_settings(self.verbose)
        self.execute()
        self.ps.set_settings(settings)
