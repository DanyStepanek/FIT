function [X labels] = rand_gmm(N, Ws, MUs, COVs)
%RAND_GAUSS  Gaussian mixture distributed random numbers.
%   X = RAND_GMM(N, Ws, MUs, COVs) returns matrix with N columns, where each 
%   column is a vector chosen from a distribution represnted by a Gaussian
%   Mixture Model. The GMM parameters are mixture component mean vectors given
%   by columns of D-by-M matrix MUs, covariance matrices given by D-by-D-by-M
%   matrix COVs and vector of weights Ws.
%
%   [X labels] = rand_gmm(N, Ws, MUs, COVs) also returs second output, which
%   is vector of mixture indices that the individual data points were generated
%   from.
%
%   RAND_GMM uses RANDN to produces pseudo-random numbers. See RANDN for more
%   details on pseudo-random numbers generation and its initialization.
%
%    Example:
%
%       Plot data generated from 2D Multivariate Gaussian distribution
%       with mean [1 1] and covariance matrix [2, 0.2; 0.2 1] and plot
%       ellipse representing this distribution.
%          x = rand_gauss(500, [1 1], [2, 0.9; 0.9 1]);
%          plot(x(1,:), x(2,:), '.');
%          hold on;
%          gellipse([1 1], [2, 0.9; 0.9 1], 100, 'r');
%
%   See also GELLIPSE, RANDN.

Ws = mnrnd(N, Ws);
X=[];
labels=[];

for ii=1:length(Ws)
  if ndims(COVs) == ndims(MUs) && all(size(COVs) == size(MUs))
    % variance vectors in case of diagonal covariance model
    X=[X rand_gauss(Ws(ii), MUs(:,ii), diag(COVs(:,ii)))];
  else
    % covariance matrices in case of full covariance model
    X=[X rand_gauss(Ws(ii), MUs(:,ii), COVs(:,:,ii))];
  end
  labels=[labels ii*ones(1, Ws(ii))];
end
perm=randperm(size(X,2));
X=X(:,perm);
labels=labels(perm);
