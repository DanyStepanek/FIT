addpath('lib');

% Generate random data for classes X1 and X2. The data for each class are
% generated from two gaussian distributions. Hopefully, we will be able to
% learn these distributions from data using EM algorithm implemented in 
% 'train_gmm' function.
X1=[rand_gauss(400, [50 40], [100 70; 70 100])  rand_gauss(200, [55 75], [25 0; 0 25])];
X2=[rand_gauss(400, [45 60], [40 0; 0 40])      rand_gauss(200, [30 40], [20 0; 0 40])];

[MU1 COV1] = train_gauss(X1);
[MU2 COV2] = train_gauss(X2);
P1 = 0.5;
P2 = 0.5;

% Plot the data
figure; hold on; 
title('Single gaussian model used for non-gaussian data')
plot([1 1j] * X1, 'r.'); 
plot([1 1j] * X2, 'b.');
gellipse(MU1, COV1, 100, 'r','LineWidth', 2);
gellipse(MU2, COV2, 100, 'b','LineWidth', 2);
ax=axis;

% Define functions which takes data as a parameter and, for our models of the two classes, ...
% make hard decision - return one to decide for calss X1 and zero otherwise
hard_decision = @(X)                  logpdf_gauss(X, MU1, COV1) + log(P1) > logpdf_gauss(X, MU2, COV2) + log(P2);

% compute posterior probability for class X1
X1_posterior  = @(X) logistic_sigmoid(logpdf_gauss(X, MU1, COV1) + log(P1) - logpdf_gauss(X, MU2, COV2) - log(P2));

% Plot the data with hard decision on background
figure; hold on; 
title('Single gaussian model - hard decision')
plot2dfun(hard_decision, ax, 1000);
plot([1 1j] * X1, 'r.'); 
plot([1 1j] * X2, 'b.');
gellipse(MU1, COV1, 100, 'r','LineWidth', 2); 
gellipse(MU2, COV2, 100, 'b','LineWidth', 2);


% Plot the data with hard posterior probability as background
figure; hold on;
title('Single gaussian model - posterior probability of class X1')
plot2dfun(X1_posterior, ax, 1000);
plot([1 1j] * X1, 'r.'); 
plot([1 1j] * X2, 'b.');
gellipse(MU1, COV1, 100, 'r','LineWidth', 2); 
gellipse(MU2, COV2, 100, 'b','LineWidth', 2);


% Train and test with GMM models with full covariance matrices
%Decide for number of gaussian mixture components used for the model
M1=2;  % budeme mit 2 Gaussovky

% Initialize mean vectors, covariance matrices and weights of mixture componments
% Initialize mean vectors to randomly selected data points from corresponding class
MUs1  = X1(:,random('unid', size(X1,2), 1, M1));

% Initialize all covariance matrices to the same covariance matrices computed using
% all the data from the given class
COVs1 = repmat(COV1, [1 1 M1]); % indexing by the 3rd dimension 

% Use uniform distribution as initial guess for the weights
Ws1    = ones(1,M1) / M1;

% Initialize parameters of the second model
M2=2;
MUs2  = X2(:,random('unid', size(X2,2), 1, M2));  
COVs2 = repmat(COV2, [1 1 M2]); % indexing by the 3rd dimension 
Ws2    = ones(1,M2) / M2;

% Run 30 iterations of EM algorithm to train the two GMM models
figure;
for jj=1:30
  clf; hold on
  % plot the data and elipses representing the updated gaussian distributios 
  plot([1 1j] * X1, 'r.'); 
  plot([1 1j] * X2, 'b.');

  for ii = 1:M1, gellipse(MUs1(:,ii), COVs1(:,:,ii), 100,'r','LineWidth', round(Ws1(ii)*10)); end
  for ii = 1:M2, gellipse(MUs2(:,ii), COVs2(:,:,ii), 100,'b','LineWidth', round(Ws2(ii)*10)); end

  %reestimate parameters ot the two models
  [Ws1, MUs1, COVs1, TTL1] = train_gmm(X1, Ws1, MUs1, COVs1); 
  [Ws2, MUs2, COVs2, TTL2] = train_gmm(X2, Ws2, MUs2, COVs2); 

  % report total log-likeligood showing the improvements in models fitting the data distributions.
  disp(['Total log-likelihood: ' num2str(TTL1) ' for class X1; ' num2str(TTL2) ' for class X2' ])
  pause
end
ax=axis;

% Again, show data and hard decision and posterior probabilities, this time for GMM models
hard_decision = @(X)                  logpdf_gmm(X,Ws1,MUs1,COVs1)+log(P1) > logpdf_gmm(X,Ws2,MUs2,COVs2)+log(P2);
X1_posterior  = @(X) logistic_sigmoid(logpdf_gmm(X,Ws1,MUs1,COVs1)+log(P1) - logpdf_gmm(X,Ws2,MUs2,COVs2)-log(P2));

figure; hold on; 
title('Gaussian mixture model - hard decision')
plot2dfun(hard_decision, ax, 1000);
plot([1 1j] * X1, 'r.'); 
plot([1 1j] * X2, 'b.');
for ii = 1:M1, gellipse(MUs1(:,ii), COVs1(:,:,ii), 100,'r','LineWidth', round(Ws1(ii)*10)); end
for ii = 1:M2, gellipse(MUs2(:,ii), COVs2(:,:,ii), 100,'b','LineWidth', round(Ws2(ii)*10)); end

figure; hold on; 
title('Gaussian mixture model - posterior probability of class X1')
plot2dfun(X1_posterior, ax, 1000);
plot([1 1j] * X1, 'r.'); 
plot([1 1j] * X2, 'b.');
for ii = 1:M1, gellipse(MUs1(:,ii), COVs1(:,:,ii), 100,'r','LineWidth', round(Ws1(ii)*10)); end
for ii = 1:M2, gellipse(MUs2(:,ii), COVs2(:,:,ii), 100,'b','LineWidth', round(Ws2(ii)*10)); end
