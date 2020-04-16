addpath('lib');

figure; hold on; 
X1=rand_gauss(100, [50 50], [100 70; 70 100]); plot([1 1j] * X1, 'r.'); 
X2=rand_gauss(100, [40 60], [40 0; 0 40]);     plot([1 1j] * X2, 'b.');
ax=axis;

k=9
hard_decision = @(X) k_nearest_neighbours(X, X1, X2, k) > 0.5;
soft_score    = @(X) k_nearest_neighbours(X, X1, X2, k);

figure; hold on; 
title('K nearest neighbours - hard decision')
plot2dfun(hard_decision, ax, 200);
plot([1 1j] * X1, 'r.'); 
plot([1 1j] * X2, 'b.');

figure; hold on; 
title('K nearest neighbours - soft score')
plot2dfun(soft_score, ax, 200);
plot([1 1j] * X1, 'r.'); 
plot([1 1j] * X2, 'b.');
