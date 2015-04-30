findrarity <- function(mids, counts, dmag) {
    if (dmag > 0) {
        locs=which(mids >= dmag)
    }
    if (dmag <= 0) {
        locs=which(mids <= dmag)
    }
    #object is 1 in rarity number of events, so this can be greater
    #than the number of stars in the field (105000, in this case) For
    #l=96, b=-60, 1 in a million is probably when you would start to
    #think it is interesting
    rarity=sum(counts)/sum(counts[locs])
    return(rarity)
}
