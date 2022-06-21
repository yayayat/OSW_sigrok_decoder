import sigrokdecode as srd


class SamplerateError(Exception):
    pass


class Decoder(srd.Decoder):
    api_version = 3
    id = 'OneSingleWire'
    name = 'OneSingleWire custom bus'
    longname = 'OneSingleWire custom bus used in roboSet'
    desc = 'Bidirectional, half-duplex, asynchronous serial bus.'
    license = 'gplv2+'
    inputs = ['logic']
    outputs = ['OneSingleWire']
    tags = ['Custom']
    channels = (
        {'id': 'osw', 'name': 'OSW', 'desc': 'OSW signal line'},
    )

    annotations = (
        ('bit', 'Bit'),
    )
    annotation_rows = (
        ('bits', 'Bits', (0,)),
    )

    def start(self):
        self.out_ann = self.register(srd.OUTPUT_ANN)

    def reset(self):
        pass

    def metadata(self, key, value):
        if key == srd.SRD_CONF_SAMPLERATE:
            self.threshold_samples_num = int(8.3 * (value / 1000000.0))

    def decode(self):
        self.wait({0: 'f'})
        self.bt_block_ss = self.samplenum
        while True:
            self.wait({0: 'e'})
            period_range = self.samplenum - self.bt_block_ss
            if (period_range < self.threshold_samples_num):
                osw = 1
            else:
                osw = 0

            self.put(self.bt_block_ss, self.samplenum,
                     self.out_ann, [0, ['Bit: %d' % osw, '%d' % osw]])
            self.bt_block_ss = self.samplenum
