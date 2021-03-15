import unittest

import ROOT

class RooAbsRealPlotOn(unittest.TestCase):
    """
    Test for the PlotOn callable.
    """

    x = ROOT.RooRealVar("x", "x", 0, 10)

    # Create two Gaussian PDFs g1(x,mean1,sigma) anf g2(x,mean2,sigma) and
    # their parameters
    mean = ROOT.RooRealVar("mean", "mean of gaussians", 5)
    sigma1 = ROOT.RooRealVar("sigma1", "width of gaussians", 0.5)
    sigma2 = ROOT.RooRealVar("sigma2", "width of gaussians", 1)
    sig1 = ROOT.RooGaussian("sig1", "Signal component 1", x, mean, sigma1)
    sig2 = ROOT.RooGaussian("sig2", "Signal component 2", x, mean, sigma2)

    def test_wrong_kwargs(self):
        # test that AttributeError is raised 
        # if keyword does not correspong to CmdArg
        self.assertRaises(AttributeError, self.gauss.plotOn, self.data, ThisIsNotACmgArg=True)

    def test_identical_result(self):
        # Sum the signal components into a composite signal pdf
        sig1frac = ROOT.RooRealVar(
            "sig1frac", "fraction of component 1 in signal", 0.8, 0., 1.)
        sig = ROOT.RooAddPdf(
            "sig", "Signal", ROOT.RooArgList(sig1, sig2), ROOT.RooArgList(sig1frac))

        # Build Chebychev polynomial pdf
        a0 = ROOT.RooRealVar("a0", "a0", 0.5, 0., 1.)
        a1 = ROOT.RooRealVar("a1", "a1", -0.2, 0., 1.)
        bkg1 = ROOT.RooChebychev("bkg1", "Background 1",
                                x, ROOT.RooArgList(a0, a1))

        # Build expontential pdf
        alpha = ROOT.RooRealVar("alpha", "alpha", -1)
        bkg2 = ROOT.RooExponential("bkg2", "Background 2", x, alpha)

        # Sum the background components into a composite background pdf
        bkg1frac = ROOT.RooRealVar(
            "sig1frac", "fraction of component 1 in background", 0.2, 0., 1.)
        bkg = ROOT.RooAddPdf(
            "bkg", "Signal", ROOT.RooArgList(bkg1, bkg2), ROOT.RooArgList(sig1frac))

        # Sum the composite signal and background
        bkgfrac = ROOT.RooRealVar("bkgfrac", "fraction of background", 0.5, 0., 1.)
        model = ROOT.RooAddPdf(
            "model", "g1+g2+a", ROOT.RooArgList(bkg, sig), ROOT.RooArgList(bkgfrac))

        # Set up basic plot with data and full pdf
        # ------------------------------------------------------------------------------

        # Generate a data sample of 1000 events in x from model
        data = model.generate(ROOT.RooArgSet(x), 1000)

        # Plot data and complete PDF overlaid
        xframe = x.frame(ROOT.RooFit.Title(
            "Component plotting of pdf=(sig1+sig2)+(bkg1+bkg2)"))
        data.plotOn(xframe)
        model.plotOn(xframe)

        # Clone xframe for use below
        xframe2 = xframe.Clone("xframe2")

        # Plot single background component specified by object reference
        ras_bkg = ROOT.RooArgSet(bkg)
        model.plotOn(xframe, ROOT.RooFit.Components(ras_bkg), ROOT.RooFit.LineColor(ROOT.kRed))

        # Plot single background component specified by object reference
        ras_bkg = ROOT.RooArgSet(bkg)
        model.plotOn(xframe2, Components=ras_bkg, LineColor=ROOT.kRed)
        self.assertTrue(xframe.isIdentical(xframe2))


    def test_mixed_styles(self):
        # Sum the signal components into a composite signal pdf
        sig1frac = ROOT.RooRealVar(
            "sig1frac", "fraction of component 1 in signal", 0.8, 0., 1.)
        sig = ROOT.RooAddPdf(
            "sig", "Signal", ROOT.RooArgList(sig1, sig2), ROOT.RooArgList(sig1frac))

        # Build Chebychev polynomial pdf
        a0 = ROOT.RooRealVar("a0", "a0", 0.5, 0., 1.)
        a1 = ROOT.RooRealVar("a1", "a1", -0.2, 0., 1.)
        bkg1 = ROOT.RooChebychev("bkg1", "Background 1",
                                x, ROOT.RooArgList(a0, a1))

        # Build expontential pdf
        alpha = ROOT.RooRealVar("alpha", "alpha", -1)
        bkg2 = ROOT.RooExponential("bkg2", "Background 2", x, alpha)

        # Sum the background components into a composite background pdf
        bkg1frac = ROOT.RooRealVar(
            "sig1frac", "fraction of component 1 in background", 0.2, 0., 1.)
        bkg = ROOT.RooAddPdf(
            "bkg", "Signal", ROOT.RooArgList(bkg1, bkg2), ROOT.RooArgList(sig1frac))

        # Sum the composite signal and background
        bkgfrac = ROOT.RooRealVar("bkgfrac", "fraction of background", 0.5, 0., 1.)
        model = ROOT.RooAddPdf(
            "model", "g1+g2+a", ROOT.RooArgList(bkg, sig), ROOT.RooArgList(bkgfrac))

        # Set up basic plot with data and full pdf
        # ------------------------------------------------------------------------------

        # Generate a data sample of 1000 events in x from model
        data = model.generate(ROOT.RooArgSet(x), 1000)

        # Plot data and complete PDF overlaid
        xframe = x.frame(ROOT.RooFit.Title(
            "Component plotting of pdf=(sig1+sig2)+(bkg1+bkg2)"))
        data.plotOn(xframe)
        model.plotOn(xframe)

        # Clone xframe for use below
        xframe2 = xframe.Clone("xframe2")

        # Plot single background component specified by object reference
        ras_bkg = ROOT.RooArgSet(bkg)
        model.plotOn(xframe, ROOT.RooFit.Components(ras_bkg), ROOT.RooFit.LineColor(ROOT.kRed))

        # Plot single background component specified by object reference
        ras_bkg = ROOT.RooArgSet(bkg)
        model.plotOn(xframe2, ROOT.RooFit.LineColor(ROOT.kRed), Components=ras_bkg)
        self.assertTrue(xframe.isIdentical(xframe2))


if __name__ == '__main__':
    unittest.main()


