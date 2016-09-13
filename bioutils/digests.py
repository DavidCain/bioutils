# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import base64
import hashlib
import re

import six


def _to_binary(s):
    return s if isinstance(s, six.binary_type) else s.encode()


def normalize_sequence(seq):
    """return normalized representation of sequence for hashing

    This really means removing whitespace and asterisks and
    uppercasing.

    """

    seq = _to_binary(seq)
    return re.sub(b"[\s\*]", b"", seq).upper()


def seq_seguid(seq, normalize=True):
    """returns seguid for sequence `seq`

    This seguid is compatible with BioPython's seguid.

    >>> seq_seguid('')
    '2jmj7l5rSw0yVb/vlWAYkK/YBwk'

    >>> seq_seguid('ACGT')
    'IQiZThf2zKn/I1KtqStlEdsHYDQ'

    >>> seq_seguid('acgt')
    'IQiZThf2zKn/I1KtqStlEdsHYDQ'

    >>> seq_seguid('acgt', normalize=False)
    'lII0AoG1/I8qKY271rgv5CFZtsU'

    """ 
    seq = _to_binary(seq)
    seq = normalize_sequence(seq) if normalize else seq
    return base64.b64encode(hashlib.sha1(seq).digest()).decode("ascii").rstrip('=')


def sha512t(data, digest_size=24):
    """returns ASCII seqhash hash for sequence `seq`

    Following the logic in http://stackoverflow.com/a/4014407/342839,
    the probability of a collision using b bits with m messages (sequences) is
    P(collision) = m^2 / 2^(b+1).  Solving for the number of messages:

       p = ( P(collision) * 2^(b+1) )^(1/2)

    If we arbitrarily want P(collision) < 10^-20 for 192 bits, then m = 1.12e+19. 
    That is, for ~10^19 sequences, there's a 1/10^20 probability of collision.
    This seems good enough to me.

    """ 
    return base64.urlsafe_b64encode(hashlib.sha512(data).digest()[:digest_size]).decode("ascii")


def seq_seqhash(seq, normalize=True, digest_size=24):
    """returns ASCII seqhash hash for sequence `seq`

    The seqhash hash is modelled on seguid with the following observations::

    * sha512 is 2x faster than sha1 on modern 64-bit platforms
    * 512 bits (64 bytes) is far more than is necessary. So, use 512
      for speed, but truncate for desired relative uniqueness
    * seqhash uses "url-safe" base64 alphabet (https://tools.ietf.org/html/rfc3548#section-4)
    * the gain (in decreased encoded size) isn't worth base85 encoding

    >>> seq_seqhash("")
    'z4PhNX7vuL3xVChQ1m2AB9Yg5AULVxXc'

    >>> seq_seqhash("ACGT")
    'aKF498dAxcJAqme6QYQ7EZ07-fiw8Kw2'

    >>> seq_seqhash("acgt")
    'aKF498dAxcJAqme6QYQ7EZ07-fiw8Kw2'

    >>> seq_seqhash("acgt", normalize=False)
    'eFwawHHdibaZBDcs9kW3gm31h1NNJcQe'

    """

    seq = _to_binary(seq)
    seq = normalize_sequence(seq) if normalize else seq
    return sha512t(seq, digest_size=24)




def seq_md5(seq, normalize=True):
    """returns md5 as hex digest for sequence `seq`.

    >>> seq_md5('')
    'd41d8cd98f00b204e9800998ecf8427e'

    >>> seq_md5('ACGT')
    'f1f8f4bf413b16ad135722aa4591043e'

    >>> seq_md5('ACGT*')
    'f1f8f4bf413b16ad135722aa4591043e'

    >>> seq_md5(' A C G T ')
    'f1f8f4bf413b16ad135722aa4591043e'

    >>> seq_md5('acgt')
    'f1f8f4bf413b16ad135722aa4591043e'

    >>> seq_md5('acgt', normalize=False)
    'db516c3913e179338b162b2476d1c23f'

    """
    seq = _to_binary(seq)
    seq = normalize_sequence(seq) if normalize else seq
    return hashlib.md5(seq).hexdigest()


def seq_sha1(seq, normalize=True):
    """returns sequence sha1 hexdigest for sequence `seq`.

    >>> seq_sha1('')
    'da39a3ee5e6b4b0d3255bfef95601890afd80709'

    >>> seq_sha1('ACGT')
    '2108994e17f6cca9ff2352ada92b6511db076034'

    >>> seq_sha1('acgt')
    '2108994e17f6cca9ff2352ada92b6511db076034'

    >>> seq_sha1('acgt', normalize=False)
    '9482340281b5fc8f2a298dbbd6b82fe42159b6c5'

    """

    seq = _to_binary(seq)
    seq = normalize_sequence(seq) if normalize else seq
    return hashlib.sha1(seq).hexdigest()


def seq_sha512(seq, normalize=True):
    """returns sequence sha512 hexdigest for sequence `seq`.

    >>> seq_sha512('')
    'cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e'

    >>> seq_sha512('ACGT')
    '68a178f7c740c5c240aa67ba41843b119d3bf9f8b0f0ac36cf701d26672964efbd536d197f51ce634fc70634d1eefe575bec34c83247abc52010f6e2bbdb8253'

    >>> seq_sha512('acgt')
    '68a178f7c740c5c240aa67ba41843b119d3bf9f8b0f0ac36cf701d26672964efbd536d197f51ce634fc70634d1eefe575bec34c83247abc52010f6e2bbdb8253'

    >>> seq_sha512('acgt', normalize=False)
    '785c1ac071dd89b69904372cf645b7826df587534d25c41edb2862e54fb2940d697218f2883d2bf1a11cdaee658c7f7ab945a1cfd08eb26cbce57ee88790250a'

    """

    seq = _to_binary(seq)
    seq = normalize_sequence(seq) if normalize else seq
    return hashlib.sha512(seq).hexdigest()

