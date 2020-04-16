addpath('lib');

% data generation
red_data  = rand_gauss(1000, [50 50], [100 70; 70 100]); 
blue_data = rand_gauss(1000, [40 70], [40 0; 0 40]);     

hovado    = rand_gauss(80, [-20 110], [20 0; 0 20]);     
blue_data = [blue_data hovado];

X         = [red_data blue_data];
T         = [ones(1, size(red_data, 2)) zeros(1, size(blue_data, 2))];

% plot the data
figure; hold on; 
plot([1 1i] * red_data , 'r.');
plot([1 1i] * blue_data, 'b.');
ax = axis;

% initialize the parameters of the linear clasifier, i.e. weights + bias
[w w0 data_cov] = train_generative_linear_classifier(X, T);

% synthesisze the separation line and plot it (again note the projection to [1;j])
x1 = ax(1);
x2 = ax(2);
y1 = (-w0 - (w(1)*x1)) / w(2);
y2 = (-w0 - (w(1)*x2)) / w(2);
plot([x1 x2], [y1 y2], 'k', 'LineWidth', 2);
gellipse(mean(red_data,  2), data_cov, 100, 'r');
gellipse(mean(blue_data, 2), data_cov, 100, 'b');

title('Linear classifier - posterior probability of red class')
for ii=1:100
  % we plot the data points (note multiplication by [1 1i] which transforms
  % every (x,y) point to x + i*y, which is easy for matlab to plot)
  red_posterior  = @(X) logistic_sigmoid(w' * X + w0);
  plot2dfun(red_posterior, ax, 1000); hold on
  plot([1 1i] * red_data , 'r.'); 
  plot([1 1i] * blue_data, 'b.') 
  axis(ax); hold off;
  pause
  [w w0] = train_linear_logistic_regression(X, T, w, w0);
end
