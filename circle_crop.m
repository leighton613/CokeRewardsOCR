function new_filename = circle_crop(filename)
%% Author: leighton.zxw@gmail.com

rgb = imread(filename);

% figure(1); subplot(131); imshow(rgb);
% gray = rgb2gray(rgb); subplot(132); imshow(gray);

%% Find inner circle
sentivity = 0.99;
edge_th = 0.05;

[centers1, radii1] = imfindcircles(rgb,[450 550],'ObjectPolarity',...
    'dark','Sensitivity',sentivity, 'EdgeThreshold',edge_th);

% visualization:
% viscircles(centers1, radii1, 'EdgeColor', 'b');

% [centers2, radii2] = imfindcircles(rgb,[550 650],'ObjectPolarity',...
%     'dark','Sensitivity',sentivity, 'EdgeThreshold',edge_th);
% 
% [centers3, radii3] = imfindcircles(rgb,[650 750],'ObjectPolarity',...
%     'dark','Sensitivity',sentivity, 'EdgeThreshold',edge_th);
% 
% [centers4, radii4] = imfindcircles(rgb,[750 850],'ObjectPolarity',...
%     'dark','Sensitivity',sentivity, 'EdgeThreshold',edge_th);
% pause;
%% crop inside
r = radii1;
ci = [centers1(1), centers1(2)];
imageSize = size(rgb);
[xx,yy] = ndgrid((1:imageSize(1))-ci(1),(1:imageSize(2))-ci(2));

mask_in = uint8((xx.^2 + yy.^2)<r^2);
croppedIn = uint8(zeros(size(rgb)));
for i=1:3
    croppedIn(:,:,i) = rgb(:,:,i).*mask_in;
end

% background
mask_bg = uint8((xx.^2 + yy.^2)>=r^2);
croppedBG = uint8(255 * ones(size(rgb(:,:,1))));
bg = croppedBG .* mask_bg;


% background + content
for i = 1:3
    croppedIn(:,:,i) = croppedIn(:,:,i) + bg;
end

% subplot(133);imshow(croppedIn);

temp_cell = strsplit(filename, '.');
file_pure = temp_cell{1};
ext = temp_cell{2};
writeOutName = strcat(file_pure, '_circle.', ext);
imwrite(croppedIn, writeOutName);

new_filename = writeOutName;
end
