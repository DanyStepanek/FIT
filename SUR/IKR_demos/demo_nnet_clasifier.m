%%%%%%%%%%%%%% BRIEFLY
%we will do binary classification on arfificial 
%dataset which is not linearly separable,
%this will demonstrate the representative 
%power of Artificial Neural Networks (ANNs)

addpath('lib');

%%%%%%%%%%%%%% GENERATING TRAINING DATASET
%generate training data which are NOT linearly separable
N=333;
X1=randn(2,N) + repmat([1;3],1,N);
X1=[X1 randn(2,N) + repmat([-2;-2],1,N)];
X1=[X1 randn(2,N) + repmat([0;0],1,N)];

X2=randn(2,N) + repmat([-2;2],1,N);
X2=[X2 randn(2,N) + repmat([2;-2],1,N)];
X2=[X2 randn(2,N) + repmat([4;4],1,N)];
X2=[X2 randn(2,N) + repmat([-4;-4],1,N)];
%2331 training examples in total

%generate corresponding target values:
%ones for class C1, zeros for class C2
T1=ones(1,size(X1,2));
T2=zeros(1,size(X2,2));


%%%%%%%%%%%%%% NORMALIZING INPUT
% E[X]=0 D[X]=1 (ie. zero mean and unit variance)
mu=mean([X1 X2]')' %get mean
sig=std([X1 X2]')' %get variance

X1=(X1-repmat(mu,1,size(X1,2))) ./ repmat(sig,1,size(X1,2));
X2=(X2-repmat(mu,1,size(X2,2))) ./ repmat(sig,1,size(X2,2));

%%%%%%%%%%%%%% MERGE AND RANDOMIZE ORDER OF TRAINING DATA
X=[X1 X2];
T=[T1 T2];

%show the normalized data
plot(X1(1,:),X1(2,:),'rx',X2(1,:),X2(2,:),'bx');
ax=axis;
        
%%%%%%%%%%%%%% NETWORK INITIALIZATION
DIM_IN=2; %dimension of input layer
DIM_HIDDEN=5; %dimension of hidden layer, this can be adjusted
DIM_OUT=1;%dimension of output layer
%we use samples from Normal distribution: No(0,I*0.01)
W1=randn(DIM_HIDDEN,DIM_IN+1)*0.1; %+1 due to bias
W2=randn(DIM_OUT,DIM_HIDDEN+1)*0.1; %+1 due to bias

%%%%%%%%%%%%%% GLOBAL TRAINING CONSTANTS
% Epsilon is a learning rate (also step-size),
% this parameter scales the gradients and adjusts 
% the speed of the training:
% - if it is too big, the learning oscillates
% - if it is too small, the learning is slow
epsilon=0.05;

%%%%%%%%%%%%%% START TRAINING
%- this is school demo, only training set is used.
%  - normally we would monitor Error function on Cross-Validation set
%    to prevent overfitting (early stopping algorithm)
%  - also normally we would start halving the learning rate at some point,
%    however this will probably not help much because of such small training set

%now we will perform 50 iterations with fixed learning rate
for iter=1:50
  plot2dfun(@(X) eval_nnet(X,W1,W2), ax, 100); hold on;
  plot(X1(1,:),X1(2,:),'rx',X2(1,:),X2(2,:),'bx'); hold off;
  pause

  %perform one epoch of the training
  [W1,W2,Ed] = train_nnet(X,T,W1,W2,epsilon);
  disp(['Total log-likelihood: ' num2str(-Ed) '; Probability of correct per sample: ' num2str(exp(-Ed/size(X,2)))])
end
        