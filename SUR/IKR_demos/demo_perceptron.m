%red_data  = [-1 -1; 1 1]; %xor_true
%blue_data = [-1 1; 1 -1]; %xor_false 

red_data   = [ 0.2  0.7;  0.4 -0.5;  0.5  0.3;  0.7 -0.9;  0.9  0.9];
blue_data  = [-0.1 -0.2; -0.4  0.7; -0.5  0.6; -0.6  0.9; -0.7  0.5];
% hovado     = [0.5 0.3];
% blue_data  = [blue_data; hovado];

% prepare the plot
figure(1)
clf
hold on
axis([-1 1 -1 1]);

% plot the data
plot(red_data  * [1;i], '*r')
plot(blue_data * [1;i], '*b')

% initialize the weight vector w
w = [-0.1867; 0.7258]
% w = rand(2, 1);

% evaluate the separation line (given by w)
ploth1 = plot([w'; 0 0] * [1;i],  'k', 'LineWidth', 2);
ploth2 = plot([w' * 10; w' * (-10)] * [i;-1] , 'k', 'LineWidth', 2);

% t indicates the class label; 1 for red data, -1 for blue data
data  = [red_data; blue_data];
t     = [ones(size(red_data, 1), 1); -1 * ones(size(blue_data, 1), 1)];

solved = false;
while ~solved
  solved = true;
  % go over all data
  for ii = 1:size(data,1)
    % compute the score
    score = data(ii,:) * w * t(ii);

    % if the score is negative we will use it to retrain the perceptron weights
    if score < 0
      solved = false;
      plotg1 = plot(data(ii,:) * [1;i], 'go', 'MarkerSize', 12, 'LineWidth', 2);
      
      % update the weights
      w = w + data(ii,:)' * t(ii);

      pause

      delete(ploth1);
      delete(ploth2);
      ploth1 = plot([w'; 0 0] * [1;i],  'k', 'LineWidth', 2);
      ploth2 = plot([w' * 10; w' * (-10)] * [i;-1] , 'k', 'LineWidth', 2);
      delete(plotg1);
    end
  end
end
