
PoolStart;

disp('Processing...');


parfor frame = 1:size(I,3)
    
    [img(:,:,frame), sigma(frame),I1(:,:,frame)] = ACSN_core(I(:,:,frame),NA,Lambda,PixelSize,Gain,Offset,Hotspot,w);
    
end

Qscore = zeros(1,size(img,3));

if Video(1) ~= 'n' && size(img,3) > 1
    
    if Video(1) ~= 'y'
        for i = 1:size(img,3)
            Qscore(i) = metric(I1(:,:,i),img(:,:,i));
            if QM(1)=='y'
                Qmap(:,:,i) = Quality_Map(img(:,:,i),I1(:,:,i)); %#ok<*SAGROW>
            end
        end
        
    end
    
    if mean(Qscore) < .55 || Video(1) == 'y'
        
        disp('Please wait... Additional 3D denoising required')
        
        psd = mean(sigma).*(.6-mean(Qscore));
        
        
        size_y = size(img,1);
        size_x = size(img,2);
        size_z = min(10,size(img,3));
        overlap = 0;
        
        Tiles = im2tiles(img,overlap,size_x,size_y,size_z);
        parfor idx = 1:numel(Tiles)
            Tiles{idx} = Video_filtering_t(Tiles{idx},'Gauss',psd,'np',1,0);
        end
        img = tiles2im(Tiles,overlap);
        clear Tiles;
        
        
        for i = 1:size(img,3)
            Qscore(i) = metric(I1(:,:,i),img(:,:,i));
            if QM(1)=='y'
                Qmap(:,:,i) = Quality_Map(img(:,:,i),I1(:,:,i));
            end
        end
        
    end
    
else
    
    for i = 1:size(img,3)
        Qscore(i) = metric(I1(:,:,i),img(:,:,i));
        if QM(1)=='y'
            Qmap(:,:,i) = Quality_Map(img(:,:,i),I1(:,:,i));
        end
    end
    
end

clear I1

disp('Done!');
