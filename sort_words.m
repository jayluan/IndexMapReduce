data = load('tfidf_data.mat');
terms = data.terms;
titles = data.titles;
term_words = data.term_words;
title_words = data.title_words;
term_positions = data.term_positions;
title_positions = data.title_positions;

sorted_title_words = {};
[tiS, tiI] = sort(title_positions);
for i=1:size(tiI,1)
    sorted_title_words{i} = title_words{tiI(i)};
end

sorted_term_words = {};
[teS, teI] = sort(term_positions);
for i=1:size(teI,1)
    sorted_term_words{i} = term_words{teI(i)};
end

inter = intersect(sorted_title_words, sorted_term_words);
catTitleTerms = union(sorted_title_words, sorted_term_words);

finalTfidf = spalloc(61344, 544498, 11061666);
teFound = 0;
tiFound = 0;
titleIndex = 1;
termIndex = 1;
for i=1:length(catTitleTerms)
    word = catTitleTerms{i};
    if strcmp(word, sorted_term_words{termIndex}) == 1
       teCol = terms(:,termIndex);
       termIndex = termIndex + 1;
       teFound = 1;
    end
    if strcmp(word, sorted_title_words{titleIndex}) == 1
        tiCol = titles(:,titleIndex);
        titleIndex = titleIndex + 1;
        tiFound = 1;
    end
    if tiFound && teFound
        finalTfidf(:,i) = (1/3)*tiCol + (1/3)*teCol;
    elseif tiFound && ~teFound
        finalTfidf(:,i) = (1/3)*tiCol;
    else
        finalTfidf(:,i) = (1/3)*teCol;
    end
    teFound = 0;
    tiFound = 0;
    i
end