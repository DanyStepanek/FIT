function mfb = mel_filter_bank(nfft, nbands, fs, fstart, fend)

% mel_filter_bank(nfft, nbands, fs, fstart, fend) returns mel filterbank as a matrix (nfft/2+1 x nbands)
% nfft   - number of samples for FFT computation
% nbands - number of filter bank bands
% fs     - sampling frequency (Hz)
% fstart - frequency (Hz) where the first filter strats
% fend   - frequency (Hz) where the last  filter ends (default fs/2)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%computation described in AURORA-project - computation of MFCC

% Mel and inverse Mel scale warping finctions
mel_inv = @(x)(10.^(x/2595)-1)*700;
mel = @(x)2595*log10(1 + x/700);

if nargin < 5
  fend = fs/2;
end

cbin = round(mel_inv(linspace(mel(fstart), mel(fend), nbands + 2)) / fs * nfft)+1;
mfb = zeros(nfft / 2 + 1, nbands);
for ii=1:nbands
   mfb(cbin(ii):  cbin(ii+1), ii) = linspace(0, 1, cbin(ii+1) - cbin(ii)   + 1);
   mfb(cbin(ii+1):cbin(ii+2), ii) = linspace(1, 0, cbin(ii+2) - cbin(ii+1) + 1);
end
