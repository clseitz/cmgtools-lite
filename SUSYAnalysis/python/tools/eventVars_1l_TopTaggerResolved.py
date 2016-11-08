from CMGTools.TTHAnalysis.treeReAnalyzer import *
import ROOT

ROOT.gROOT.ProcessLine(".L ../../../TopTagger/TopTagger/test/libTopTagger.so")
ROOT.gROOT.ProcessLine(".L ../../../TopTagger/TopTagger/include/TopTagger.h")
ROOT.gROOT.ProcessLine(".L ../../../TopTagger/TopTagger/include/TopTaggerResults.h")
ROOT.gROOT.ProcessLine(".L ../../../TopTagger/TopTagger/include/TopTaggerUtilities.h")
from ROOT import TopTagger
from ROOT import TopTaggerResults
from ROOT import ttUtility



def get4Vec(j):
    pt = j.pt
    eta = j.eta
    phi = j.phi
    M = j.mass
    j = ROOT.TLorentzVector()
    j.SetPtEtaPhiM(pt, eta, phi, M)
    return j

class EventVars1LTopTaggerResolved:
    def __init__(self):
        self.tt = TopTagger()
        self.tt.setCfgFile("../../../TopTagger/TopTagger/test/Example_TopTagger.cfg")        

        self.branches = [
            # Top related
            "test"
            ]

    def listBranches(self):
        return self.branches[:]

    def __call__(self,event,base={}):
        ret = {}
        ret['test'] = 1

        jet_collection = [j for j in Collection(event,"Jet","nJet")]

        jets  = ROOT.std.vector(ROOT.TLorentzVector)()
        btaginfo = ROOT.std.vector( float ) ()
        for jet in jet_collection:
            jets.push_back(get4Vec(jet))
            btaginfo.push_back(jet.btagCSV)

        print btaginfo[0]
#        ROOT.std.vector<ROOT.Constituent> constituents = ROOT.packageCandidates(jets, btaginfo);

        constituents = ROOT.std.vector(ROOT.Constituent)( )

        constituents = ttUtility.packageConstituents(jets, btaginfo)

        
        
        print self.tt


        return ret

if __name__ == '__main__':
    from sys import argv
    file = ROOT.TFile(argv[1])
    tree = file.Get("tree")
    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf = EventVars1LTopTaggerResolved()
        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: leps %d" % (ev.run, ev.lumi, ev.evt, ev.nLepGood)
#            tree.Show(0)
            print self.sf(ev)
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 50)
