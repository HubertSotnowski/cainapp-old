import math
import numpy as np

import torch
import torch.nn as nn

from .common3d import *


class Encoder(nn.Module):
    def __init__(self, in_channels=3, depth=3):
        super(Encoder, self).__init__()

        # Shuffle pixels to expand in channel dimension
        # shuffler_list = [PixelShuffle(0.5) for i in range(depth)]
        # self.shuffler = nn.Sequential(*shuffler_list)
        self.shuffler = PixelShuffle(1 / 2**depth)

        relu = nn.LeakyReLU(0.2, True)
        
        # FF_RCAN or FF_Resblocks
        self.interpolate = Interpolation(5, 12, in_channels * (4**depth), act=relu)
        
    def forward(self, x1, x2,x3):
        """
        Encoder: Shuffle-spread --> Feature Fusion --> Return fused features
        """
        feats1 = self.shuffler(x1)
        feats2 = self.shuffler(x2)
        feats3 = self.shuffler(x3)
        feats = self.interpolate(feats1, feats2, feats3)

        return feats


class Decoder(nn.Module):
    def __init__(self, depth=3):
        super(Decoder, self).__init__()

        # shuffler_list = [PixelShuffle(2) for i in range(depth)]
        # self.shuffler = nn.Sequential(*shuffler_list)
        self.shuffler = torch.nn.PixelShuffle(2**depth)

    def forward(self, feats):
        batch_size, channels, in_height, in_width,depth  = feats.size()
        print(feats.size())
        out=torch.unbind(feats, dim=-1)
        out1 = self.shuffler(out[0])
        out2= self.shuffler(out[1])
        #out3= self.shuffler(out[3])
        #return out1,out2,out3
        return out1,out2


class CAIN(nn.Module):
    def __init__(self, depth=3):
        super(CAIN, self).__init__()
        
        self.encoder = Encoder(in_channels=3, depth=depth)
        self.decoder = Decoder(depth=depth)
    #def forward(self, x1, x2,x3):
    def forward(self, x1, x2,x3):
        x1, m1 = sub_mean(x1)
        x2, m2 = sub_mean(x2)
        x3, m3 = sub_mean(x3)


        feats = self.encoder(x1, x2,x3)
        #feats = self.encoder(x1, x2,x3)
        out = self.decoder(feats)

        
        mi1 = (m1 + m2) / 2
        mi2 = (m2 + m3) / 2
        out1=out[0]
        out2=out[1]
        out1 += mi1
        out2 += mi2

        return out1,out2, feats
