# Copyright (C) 2021 Hyunwoong Ko <kevin.brain@kakaobrain.com> and Sang-Kil Park <skpark1224@hyundai.com>
# All rights reserved.

from kss._modules.morphemes.split_morphemes import split_morphemes
from kss._modules.sentences.split_sentences import split_sentences
from kss._modules.summarization.summarize_sentences import summarize_sentences

__ALL__ = [split_sentences, split_morphemes, summarize_sentences]
__version__ = "5.2.0"
