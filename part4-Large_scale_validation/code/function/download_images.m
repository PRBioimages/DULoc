function [img_Id,stopwhile] = download_images(ImgUrl, img_save_dir,param)
%DOWNLOAD_IMAGES download the images

% get imgname
imgurl_split = strsplit(ImgUrl, '/');
img = imgurl_split{length(imgurl_split)};
img_Id = '';
stopwhile = 0;
% download imgs with loop
for i=1:5
    try
        green_raw_img = imread(strrep(ImgUrl,param,'green'));
        blue_raw_img = imread(strrep(ImgUrl,param,'blue'));
        red_raw_img = imread(strrep(ImgUrl,param,'red'));
        yellow_raw_img = imread(strrep(ImgUrl,param,'yellow'));
        stopwhile = 1;
        
        [gh,gw,gd]=size(green_raw_img);
        [bh,bw,bd]=size(blue_raw_img);
        [rh,rw,rd]=size(red_raw_img);
        [yh,yw,yd]=size(yellow_raw_img);
        if ~((gh==gw)&&(bh==bw)&&(rh==rw)&&(yh==yw))
            stopwhile = 0;
        end
    catch ErrorInfo
        disp(ErrorInfo)
        stopwhile = 0;
    end
    
    if stopwhile
        break;
    else
        disp('continue looping')
    end
end

% write imgs
if stopwhile
    green_img = green_raw_img(:,:,2);
    blue_img = blue_raw_img(:,:,3);
    red_img = red_raw_img(:,:,1);
    yellow_img = rgb2gray(yellow_raw_img);

    img_Id = strrep(img,['_' param '.jpg'],'');
    disp(img_Id)
    imwrite(green_img,[img_save_dir '\' strrep(img,param,'green') ]);
    imwrite(blue_img,[img_save_dir '\' strrep(img,param,'blue')]);
    imwrite(red_img,[img_save_dir '\' strrep(img,param,'red')]);
    imwrite(yellow_img,[img_save_dir '\' strrep(img,param,'yellow')]);
end
end

