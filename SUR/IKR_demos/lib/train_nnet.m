function [W1,W2,Ed] = train_nnet(X,T,W1,W2,epsilon)
%TRAIN_NNET Single iteration of Stochastic Gradient Descent 
%training algorithm for Arificial Neural Networks 
%(ie. on-line backpropagation alg.)
% [W1,W2,Ed] = train_nnet(X,T,W1,W2,epsilon)
%
% X are the input features, datapoints are stored column-wise
% T target variables (0/1)
% W1 weights of 1st layer (first column contain bias)
% W2 weights of 2nd layer (first column contain bias)
% epsilon learning rate
% Ed accumulated error on the training set

%%%%%%%%%%%%%% RE-SHUFFLE THE DATA ON EACH ITERATION
mixer=randperm(size(X,2)); %use shuffling mask of indices...
X=X(:,mixer);
T=T(:,mixer);

%%%%%%%%%%%%%% PERFORM ONE EPOCH OF THE TRAINING
% The implemnted algorithm is: Stochastic Gradient Descent
% (on-line training)

Ed=0; %reset the error accumulator

%The weight updates are performed after 
%getting gradient from each datapoint 
for d_idx=1:size(X,2)
  %select the feature-target pair
  x=X(:,d_idx); 
  t=T(:,d_idx);

  %VARIABLE NAMING:
  %x ... input layer
  %h ... hidden layer
  %y ... output layer
  %W1 ... weight matrix for first layer of neurons
  %W2 ... weight matrix for second layer of neurons

  %%% PROPRAGATION
  h=logistic_sigmoid(W1*[1; x]);
  y=logistic_sigmoid(W2*[1; h]);
  
  %%% BACKPROPAGATION
  % error on activation of second layer neurons
  % dE_dy = -t.*1/y + (1-t).*1/(1-y); % d E/d y
  % dy_da2 = y.*(1-y);                % d y/d a       
  % dE_da2 = dE_dy .* dy_da2
  % simplifies to:
  dE_da2 = y - t;
  
  %error on hidden layer level, don't backpropagate by bias which is in the first column of the weight matrix
  dE_dh = W2(:,2:end)' * dE_da2;
  
  %error on activation of first layer neurons
  dE_da1 = dE_dh .* h.*(1-h); 
  
  %%% WEIGHT UPDATE
  W1=W1-epsilon*(dE_da1*[1 x']);
  W2=W2-epsilon*(dE_da2*[1 h']);

  %accumulate the  Cross Entropy objective
  Ed = Ed + -(t.*log(y) + (1-t).*log(1-y));
end
