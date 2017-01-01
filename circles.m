% Author % leighton.zxw@gmail.com

rgb = imread('./test image/cap1.jpg');
% figure(1); subplot(121); imshow(rgb);
% gray = rgb2gray(rgb); subplot(122); imshow(gray);

%% Find inner circle
sentivity = 0.99;
edge_th = 0.05;

[centers1, radii1] = imfindcircles(rgb,[450 550],'ObjectPolarity',...
    'dark','Sensitivity',sentivity, 'EdgeThreshold',edge_th);

imshow(gray);
viscircles(centers1, radii1, 'EdgeColor', 'b');
% [centers2, radii2] = imfindcircles(rgb,[550 650],'ObjectPolarity',...
%     'dark','Sensitivity',sentivity, 'EdgeThreshold',edge_th);
% 
% [centers3, radii3] = imfindcircles(rgb,[650 750],'ObjectPolarity',...
%     'dark','Sensitivity',sentivity, 'EdgeThreshold',edge_th);
% 
% [centers4, radii4] = imfindcircles(rgb,[750 850],'ObjectPolarity',...
%     'dark','Sensitivity',sentivity, 'EdgeThreshold',edge_th);
pause;
%%
% crop inside
mask_in = uint8((xx.^2 + yy.^2)<ci(3)^2);
croppedIn = uint8(zeros(size(rgb)));
for i=1:3
    croppedIn(:,:,i) = rgb(:,:,i).*mask;
end

% background
mask_bg = uint8((xx.^2 + yy.^2)>=ci(3)^2);
croppedBG = uint8(255 * ones(size(rgb(:,:,1))));
bg = croppedBG .* mask_bg;


% background + content
for i = 1:3
    croppedIn(:,:,i) = croppedIn(:,:,i) + bg;
end

imshow(croppedIn);
imwrite(croppedIn, './test image/cap1_crop.jpg');
