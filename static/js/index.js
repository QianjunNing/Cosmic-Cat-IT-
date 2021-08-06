function imageAutoChange() {
    /* Get the array object for the image and index */
    var $imgs = $("#main_div_img li");
    var $nums = $("#main_div_num li");
 
    var isStop = false;
    var index = 0;
 
    $nums.eq(index).addClass("numsover").siblings().removeClass("numsover");
    $imgs.eq(index).show();
 
    /* Mouse over the number of events handled */
    $nums.mouseover(function() {
        isStop = true;
        
        $(this).addClass("numsover").siblings().removeClass("numsover");
 
        
        index = $nums.index(this);
        $imgs.eq(index).show("slow");
        $imgs.eq(index).siblings().hide("slow");
    }).mouseout(function() {
        isStop = false
    });
    /* set loop */
    setInterval(function() {
        if(isStop) return;
        if(index >= 6) index = -1;
        index++;
 
        $nums.eq(index).addClass("numsover").siblings().removeClass("numsover");
        $imgs.eq(index).show("slow").siblings().hide("slow");
 
    }, 2000);
 
 
 
}
