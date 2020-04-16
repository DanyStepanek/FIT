function [features file_names sizes] = png2fea(dir_name)

D=dir([dir_name '/*.png']);
file_names = {D.name};
for ii=1:length(file_names)
  disp(['Processing file: ' dir_name '/' file_names{ii}])
  s = imread([dir_name '/' file_names{ii}]);
  s = double(rgb2gray(s));
  features{ii} = s(:);
  sizes{ii}    = size(s);
end
