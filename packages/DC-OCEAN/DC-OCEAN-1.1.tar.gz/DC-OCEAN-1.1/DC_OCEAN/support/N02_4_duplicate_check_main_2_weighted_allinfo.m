%%% Using mapminmax normalize each line of data, calculate the weighted average by entropy weight method, and then compare which is closer
%%% Use all of the metadata

clear
clc

for nian=1975:1975
    
    eval(['load DNA_summary_',num2str(nian),'.mat'])
    
    DNA_series_copy=DNA_series;
    DNA_series_copy(:,20)=[]; % WMO ID information is small, delete
    
    DNA_mapped=normalizeData(DNA_series_copy',0,1);
    DNA_mapped=DNA_mapped';
    DNA_mapped(DNA_series_copy==0)=0;
    
    %%% Use entropy weight method to calculate the weight
    [weight]=entropy_weight(DNA_series_copy);
    
    %%% Calculate the weighted average
    average_DNA_single=NaN(size(DNA_mapped));
    for i=1:length(weight)
        average_DNA_single(:,i)=DNA_mapped(:,i)*weight(i);
    end
    average_DNA=sum(average_DNA_single,2,'omitnan');
      
    %%% Sort average_DNA in ascending order to facilitate the establishment of the later search algorithm
    [average_DNA,index]=sort(average_DNA);
    filename_info=filename_info(index,:);
    DNA_mapped=DNA_mapped(index,:);
    DNA_series=DNA_series(index,:);
    
    %%% Cyclic search
    output_variables=['filename',variable_name];
    
    filename=['./potential_duplicates_output/',num2str(nian),'/potential_duplicate_',num2str(nian),'_weight_allinfo.txt']
    if(exist(filename))
        delete(filename)
    end
    fid=fopen(filename,'w+');
  
    number_pairs=0;
    number_profiles=0;
    for i=1:length(average_DNA)
        i
        number1=average_DNA(i);
        difference=abs((number1-average_DNA)/number1*100);   % Calculation of percentage difference
        difference(1:i-1)=NaN;
        duplicate_number=sum(difference<0.0001);   % threshold value: 0.0001%
        if(duplicate_number>=2)
            %%% potiential duplicate
            difference(i)=NaN;
            id=[i;find(difference==nanmin(difference))];
            DNA_series_small=DNA_series(id,:);
            
            %%% If it's buoy data(MRB), skip
            if(DNA_series(i,2)==7)
                continue
            end
            
            %%% Depth or temperature or salinity are scaled or translation, direct output
            if(any(abs(DNA_series_small(1,[33,34])-DNA_series_small(2,[33,34]))<1e-4)) 
                %%% Output filename
                for m=1:length(id)
                    fprintf(fid,'%s ',filename_info(id(m),:));
                end
                fprintf(fid,'\n');
                
                number_pairs=number_pairs+1;
                number_profiles=number_profiles+duplicate_number;
                continue
            end
            
            %%% Calculate how many similar fragments there are
            fragment_same_number=sum(abs(DNA_series_small(1,:)-DNA_series_small(2,:))<1e-5,'omitnan');
            if(fragment_same_number<27)  % less than 27
                continue
            end  

            %%% If it is XBT CTD MBT BOT; the location difference is plus or minus 5 degrees within a month; the same probe----excludes navigation continuous observation
            %%% If type,platform, and vehicle are the same, but sum_temp,corr(temp,depth) are different, it is judged to be multiple observations on the same survey ship/platform on the same route
            if((DNA_series_small(1,2)==4 && DNA_series_small(2,2)==4) || (DNA_series_small(1,2)==2 && DNA_series_small(2,2)==2) || (DNA_series_small(1,2)==1 && DNA_series_small(2,2)==1) || (DNA_series_small(1,2)==3 && DNA_series_small(2,2)==3))
                index1=all(DNA_series_small(1,[5,6,8,23,24,26])==DNA_series_small(2,[5,6,8,23,24,26])); 
                index2= abs(DNA_series_small(1,27)-DNA_series_small(2,27))>0.099; % sum_temp is different
                index3= abs(DNA_series_small(1,33)-DNA_series_small(2,33))>0.001; % cor_temp_depth is different  
                index4=any(abs(DNA_series_small(1,[3,4])-DNA_series_small(2,[3,4]))<5) && any(abs(DNA_series_small(1,[3,4])-DNA_series_small(2,[3,4]))>1e-5);
                if(index1 && index2 && index3 && index4)
                    continue
                end
            end
            %%% Exclude long-term continuous observation of fixed points/nearby points(MRB��Bottle��SUR)
            if((DNA_series_small(1,2)==1 && DNA_series_small(2,2)==1) || (DNA_series_small(1,2)==7 && DNA_series_small(2,2)==7) || (DNA_series_small(1,2)==5 && DNA_series_small(2,2)==5))
                index1=all(DNA_series_small(1,[5,6,8,9,22,23,24])==DNA_series_small(2,[5,6,8,9,22,23,24]));  
                index2=abs(DNA_series_small(1,27)-DNA_series_small(2,27))>0.05; % sum_temp is different
                index3=abs(DNA_series_small(1,29)-DNA_series_small(2,29))<1e-5; % sum_depth is same
                index4=all(abs(DNA_series_small(1,[3,4])-DNA_series_small(2,[3,4]))<0.01);  % fixed point: latitude and longitude less than 0.01 degree
                if(index1 && index2 && index3 && index4)
                    continue
                end
            end
                      
            %%% Output filename
            for m=1:length(id)
                fprintf(fid,'%s ',filename_info(id(m),:));
            end
            fprintf(fid,'\n');
            
            number_pairs=number_pairs+1;
            number_profiles=number_profiles+duplicate_number;
            
        end
    end
    
    number_pairs
    number_profiles
end
%%
% figure();
% plot(average_DNA,'o');
% ylabel('Average DNA')