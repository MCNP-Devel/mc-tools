#!/usr/bin/env python3
#
# https://github.com/kbat/mc-tools
#

import argparse
from sys import exit
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

# runs in both Python 2 and 3
try:
        input = raw_input
except NameError:
        pass

def main():
	"""A simple TH1/TGraph plotter
	"""
	parser = argparse.ArgumentParser(description=main.__doc__,
                                         formatter_class=argparse.ArgumentDefaultsHelpFormatter,
					 epilog="Homepage: https://github.com/kbat/mc-tools")
	parser.add_argument('dfile', type=str, help='Data file name')
	parser.add_argument('dhist', type=str, help='Data object name')
        parser.add_argument("-scale", type=float, dest='scale', help='Scale', default=1.0)
        parser.add_argument("-doption", type=str, dest='doption', help='Data draw option', default="colz")
        parser.add_argument("-title", type=str, dest='title',   help='Plot title',   default=None)
        parser.add_argument("-xtitle", type=str, dest='xtitle', help='x-axis title', default=None)
        parser.add_argument("-ytitle", type=str, dest='ytitle', help='y-axis title', default=None)
        parser.add_argument("-logx", action='store_true', default=False, dest='logx', help='Set log scale for the horizontal axis')
        parser.add_argument("-logy", action='store_true', default=False, dest='logy', help='Set log scale for the vertical axis')
        parser.add_argument("-o", type=str, dest='output', help='Output file name. If given then the canvas is not shown.', default="")

	args = parser.parse_args()

        ROOT.gStyle.SetOptStat(False)
        ROOT.gStyle.SetPalette(ROOT.kTemperatureMap)

        if args.output:
                ROOT.gROOT.SetBatch(True)

        df = ROOT.TFile(args.dfile)
        dh = df.Get(args.dhist)

        dh.Scale(args.scale)

        if args.title:
            dh.SetTitle(args.title)

        if args.xtitle:
            dh.SetXTitle(args.xtitle)
            
        if args.ytitle:
            dh.SetYTitle(args.ytitle)
            
        dh.Draw(args.doption)

        ROOT.gPad.SetLogx(args.logx)
        ROOT.gPad.SetLogy(args.logy)

        if args.output:
                ROOT.gPad.Print(args.output)
        else:
                ROOT.gPad.GetCanvas().ToggleEventStatus()
                input()

if __name__ == "__main__":
    exit(main())
