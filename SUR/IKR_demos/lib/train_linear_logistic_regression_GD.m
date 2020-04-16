function [W W0] = train_linear_logistic_regression_GD(X, class_ids, Wold, W0old, learning_rate)
%TRAIN_LLR_NR Reestimates Linear classifier parameters using Linear Logistic
% Regression, making one gradient descent step.

if nargin < 5
  learning_rate = 0.003 / size(X,2);
end
% artificially add one more dimension to the data with value "1". 
% This will infer the bias parameter
X     = [X; ones(1,size(X,2))];
Wold  = [Wold; W0old];

% compute the posteriors from the log likelihood ratios
posteriors = logistic_sigmoid(Wold' * X);
Wnew =  Wold - learning_rate * X * (posteriors - class_ids)';

W = Wnew(1:(end-1),1);
W0 = Wnew(end,1);
