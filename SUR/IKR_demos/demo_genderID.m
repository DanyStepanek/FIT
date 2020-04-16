%Read all the training and test data into cell-arrays 
addpath('lib');


train_m = raw8khz2mfcc('gID_data/male/train');
train_f = raw8khz2mfcc('gID_data/female/train');
[test_m files_m] = raw8khz2mfcc('gID_data/male/test');
[test_f files_f] = raw8khz2mfcc('gID_data/female/test');


% For training, wi do not need to know which frame come from which training
% segment. So, for each gender, concatenate all the training feature
% matrices into single matrix

train_m=cell2mat(train_m);
train_f=cell2mat(train_f);


% PCA reduction to 2 dimensions

cov_tot = cov([train_m train_f]', 1)
[e,d]=eigs(cov_tot, 2);
figure
plot([1 1j] * e' * train_m, 'b.', 'MarkerSize', 1); hold on
plot([1 1j] * e' * train_f, 'r.', 'MarkerSize', 1)

% Classes are not well separated in this subspace


% LDA reduction to 1 dimenzion (only one LDA dimension is available for 2 tridy)

n_m = size(train_m,2);
n_f = size(train_f,2);
cov_wc = (n_m*cov(train_m', 1) + n_f*cov(train_f', 1)) / (n_m + n_f);
cov_ac = cov_tot - cov_wc;
[e,d]=eigs(cov_ac, cov_wc, 1)
[hist_m x_m] = hist(e' * train_m, 40);
[hist_f x_f] = hist(e' * train_f, 40);
figure
plot(x_m, hist_m, 'b', x_f, hist_f, 'r');

% Distribution in this single dimensional space are reasonable separated


% Lets define uniform a-priori probabilities of classes:
P_m = 0.5;
P_f = 1 - P_m;


% For one male test utterance (test_m{1}), obtain frame-by-frame log-likelihoods
% with two models, one trained using male and second using feamle training data.
% In this case, the models are single gaussians with diagonal covariance matrices.

ll_m = logpdf_gauss(test_m{1}, mean(train_m')', var(train_m', 1)');
ll_f = logpdf_gauss(test_m{1}, mean(train_f')', var(train_f', 1)');


% Plot the frame-by-frame likelihoods obtained with the two models; Note that
% 'll_m' and 'll_f' are log likelihoods, so we need to use exp function
figure; plot(exp(ll_m), 'b'); hold on; plot(exp(ll_f), 'r');

% Plot frame-by-frame posteriors

posterior_m = exp(ll_m)*P_m ./(exp(ll_m)*P_m + exp(ll_f)*P_f);
% Alternatively the posterior can by computed using log-likelihood ratio and
% logistic sigmoid function as:
%    posterior_m = logistic_sigmoid(ll_m - ll_f + log(P_m/P_f));
figure; plot(posterior_m, 'b');  hold on; plot(1- posterior_m, 'r');


% Plot frame-by-frame log-likelihoods
figure; plot(ll_m, 'b'); hold on; plot(ll_f, 'r');


% But, we do not want to make frame-by-frame decisions. We want to recognize the
% whole segment. Aplying frame independeny assumption, we sum log-likelihoods.
% We decide for class 'male' if the following quantity is positive.

(sum(ll_m) + log(P_m)) - (sum(ll_f) + log(P_f))


% Repeating the whole excercise, now with gaussian models with full covariance
% matrices

ll_m = logpdf_gauss(test_m{1}, mean(train_m')', cov(train_m', 1));
ll_f = logpdf_gauss(test_m{1}, mean(train_f')', cov(train_f', 1));
posterior_m = exp(ll_m)*P_m ./(exp(ll_m)*P_m + exp(ll_f)*P_f);
figure; plot(posterior_m, 'b'); hold on; plot(1-posterior_m, 'r');
figure; plot(ll_m, 'b');        hold on; plot(ll_f, 'r');
(sum(ll_m) + log(P_m)) - (sum(ll_f) + log(P_f))


% Again gaussian models with full covariance matrices. Now testing a female
% utterance

ll_m = logpdf_gauss(test_f{1}, mean(train_m')', cov(train_m', 1));
ll_f = logpdf_gauss(test_f{1}, mean(train_f')', cov(train_f', 1));
posterior_m = exp(ll_m)*P_m ./(exp(ll_m)*P_m + exp(ll_f)*P_f);
figure; plot(posterior_m, 'b'); hold on; plot(1-posterior_m, 'r');
figure; plot(ll_m, 'b');        hold on; plot(ll_f, 'r');
(sum(ll_m) + log(P_m)) - (sum(ll_f) + log(P_f))


% Now run recognition for all male test utterances
% To do the same for females set "test_set=test_f"

[mean_m cov_m] = train_gauss(train_m);
[mean_f cov_f] = train_gauss(train_f);
test_set = test_m
for ii=1:length(test_set)
  ll_m = logpdf_gauss(test_set{ii}, mean_m, cov_m);
  ll_f = logpdf_gauss(test_set{ii}, mean_f, cov_f);
  score(ii)=(sum(ll_m) + log(P_m)) - (sum(ll_f) + log(P_f));
end
score


% Run recognition with 1-dimensional LDA projected data

[mean_m cov_m] = train_gauss(e' * train_m);
[mean_f cov_f] = train_gauss(e' * train_f);
test_set=test_m;
for ii=1:length(test_set)
  ll_m = logpdf_gauss(e' * test_set{ii}, mean_m, cov_m);
  ll_f = logpdf_gauss(e' * test_set{ii}, mean_f, cov_f);
  score(ii)=(sum(ll_m) + log(P_m)) - (sum(ll_f) + log(P_f));
end
score


% Train and test with GMM models with diagonal covariance matrices
%Decide for number of gaussian mixture components used for the male model
M_m = 2

% Initialize mean vectors, covariance matrices and weights of mixture componments
% Initialize mean vectors to randomly selected data points from corresponding class
MUs_m  = train_m(:,random('unid', size(train_m, 2), 1, M_m));  

% Initialize all variance vectors (diagonals of the full covariance matrices) to
% the same variance vector computed using all the data from the given class
COVs_m = repmat(var(train_m', 1)', 1, M_m);

% Use uniform distribution as initial guess for the weights
Ws_m   = ones(1,M_m) / M_m;


% Initialize parameters of feamele model
M_f = 5
MUs_f  = train_f(:,random('unid', size(train_f, 2), 1, M_f));  
COVs_f = repmat(var(train_f', 1)', 1, M_f);
Ws_f   = ones(1,M_f) / M_f;

% Run 30 iterations of EM algorithm to train the two GMMs from males and females
for jj=1:30
  [Ws_m, MUs_m, COVs_m, TTL_m] = train_gmm(train_m, Ws_m, MUs_m, COVs_m); 
  [Ws_f, MUs_f, COVs_f, TTL_f] = train_gmm(train_f, Ws_f, MUs_f, COVs_f); 
  disp(['Iteration: ' num2str(jj) ' Total log-likelihood: ' num2str(TTL_m) ' for males; ' num2str(TTL_f) ' for frmales' ])
end

test_set=test_m;
for ii=1:length(test_set)
  ll_m = logpdf_gmm(test_set{ii}, Ws_m, MUs_m, COVs_m);
  ll_f = logpdf_gmm(test_set{ii}, Ws_f, MUs_f, COVs_f);
  score(ii)=(sum(ll_m) + log(P_m)) - (sum(ll_f) + log(P_f));
end
score
