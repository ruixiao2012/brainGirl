var img_top_margin,img_left_margin,img_width,img_height;//最后使用的2个变量
$(function(){
    $("#addTab a").click(function(e){
        e.preventDefault();
        $(this).tab("show");
        //alert($(this).attr('href'))
        var type=$(this).attr('href');
        $('#type').val(type);
    });

  $("#file-pic").fileinput({
    overwriteInitial: true,
    maxFileCount: 1,
    uploadUrl: "/do_upload/", // server upload action
    uploadExtraData:{type:'picture',marginTop:img_top_margin,marginLeft:img_left_margin,width:img_width,height:img_height},
    previewFileType: "image",
	browseClass: "btn btn-success",
	browseLabel: "Pick Image",
	browseIcon: '<i class="glyphicon glyphicon-picture"></i>',
	//removeClass: "btn btn-danger",
	//removeLabel: "Delete",
	//removeIcon: '<i class="glyphicon glyphicon-trash"></i>',
	//uploadClass: "btn btn-info",
	//uploadLabel: "Upload",
	//uploadIcon: '<i class="glyphicon glyphicon-upload"></i>',
	showRemove: false,
	showUpload: false,
	showPreview:false,
    }).on("filebatchselected", function(event, files) {
    // trigger upload method immediately after files are selected
        $("#file-pic").fileinput("upload");
    });


    $('#file-pic').on('filebatchpreupload', function(event, data, previewId, index) {
    var form = data.form, files = data.files, extra = data.extra,
        response = data.response, reader = data.reader;
    console.log('File batch pre upload');

        //jcrop_api.release();destroy
        if(jcrop_api){
            //jcrop_api.destroy();
        }

    });
    $('#file-pic').on('filebatchuploadsuccess', function(event, data, previewId, index) {
    //var form = data.form, files = data.files, extra = data.extra,
    //    response = data.response, reader = data.reader;
    //alert(data.response.files);


    $('#attach_pic').val(data.response.files);

    //alert("hello")
    $("#img_preview").attr("src","../"+data.response.files);


    $("#img_preview-pane").attr("src","../"+data.response.files);

    $('#x1').val(0);
    $('#y1').val(0);
    $('#x2').val(0);
    $('#y2').val(0);
    $('#w').val(0);
    $('#h').val(0);

    jcrop_api.setImage("../"+data.response.files,function(){
      this.setOptions({
        bgOpacity: 1,
      });
      console.log(jcrop_api.getBounds())
      var bounds = this.getBounds();
      boundx = bounds[0];
      boundy = bounds[1];
      })

    //length=$("#"+previewId).children("img:eq(0)")[0].width
    //alert(length)


    //$('#file-pic').fileinput("disable")

    });



    $("#file-music").fileinput({
    uploadUrl: "/do_upload/", // server upload action
    uploadExtraData:{type:'audio'},
    maxFileCount: 1,
    showPreview: true,
    previewFileType: "audio",
	browseClass: "btn btn-success",
	browseLabel: "Pick Music",
	browseIcon: '<i class="glyphicon glyphicon-picture"></i>',
	removeClass: "btn btn-danger",
	removeLabel: "Delete",
	removeIcon: '<i class="glyphicon glyphicon-trash"></i>',
	uploadClass: "btn btn-info",
	uploadLabel: "Upload",
	uploadIcon: '<i class="glyphicon glyphicon-upload"></i>',
    }).on("filebatchselected", function(event, files) {
    // trigger upload method immediately after files are selected
        $("#file-music").fileinput("upload");
    });




    $('#file-music').on('fileuploaded', function(event, data, previewId, index) {
    //var form = data.form, files = data.files, extra = data.extra,
    //    response = data.response, reader = data.reader;
    //alert(data.response.files);
    length=$("#"+previewId).children("audio:eq(0)")[0].duration
    if(length<7)
    alert("歌曲不得小于7秒")
    //if(length>13)
    //alert("歌曲不得大于13秒")
    //$('#file-music').fileinput('reset');
    alert(data.response.files)
    $('#attach_music').val(data.response.files);
    });



    $('#add_question').bind('click', function () {
        var title,optionA,optionB,optionC,optionD,answer,type
        title=$('#title').val();
        optionA=$('#optionA').val();
        optionB=$('#optionB').val();
        optionC=$('#optionC').val();
        optionD=$('#optionD').val();
        answer=$('input:radio[name="optionsRadios"]:checked').val();
        attach=$('#attach').val();
        pictype=$('input:radio[name="optPicType"]:checked').val();
        //alert(pictype)

        type=$('#type').val();
        if(type=='#addpicture'){
            attach=$('#attach_pic').val();

        }else if(type=='#addmusic'){
            attach=$('#attach_music').val();
        }else{
            attach='';
        }

        url = '/do_add_question/'
        if (type!='' && title != '' && optionA != '' && optionB != '' && optionC != '' && optionD != '' && answer != '') {
            if (type!='#addpicture'){
            jQuery.ajax({
                type: 'POST',
                url: url,
                data: {
                    type:type,
                    title: title,
                    optionA: optionA,
                    optionB: optionB,
                    optionC: optionC,
                    optionD: optionD,
                    answer: answer,
                    attach:attach
                },
                success: add_question_result,
                error:error_alert,
                dataType: 'json',
                async: false,
                contentType: "application/x-www-form-urlencoded; charset=utf-8"
            });
            }else{
                jQuery.ajax({
                type: 'POST',
                url: url,
                data: {
                    type:type,
                    pictype:pictype,
                    title: title,
                    optionA: optionA,
                    optionB: optionB,
                    optionC: optionC,
                    optionD: optionD,
                    answer: answer,
                    attach:attach
                },
                success: add_picture_result,
                error:error_alert,
                dataType: 'json',
                async: false,
                contentType: "application/x-www-form-urlencoded; charset=utf-8"
            });
            }
            return false;
        }
        else {
            alert('请检查输入是否为空！')
        }

    });





    // Create variables (in this scope) to hold the API and image size
    var jcrop_api,
    boundx,
    boundy,

    // Grab some information about the preview pane
    $preview = $('#preview-pane'),
    $pcnt = $('#preview-pane .preview-container'),
    $pimg = $('#preview-pane .preview-container img'),

    xsize = $pcnt.width(),
    ysize = $pcnt.height();
    console.log('init',[xsize,ysize]);
    $('#img_preview').Jcrop({
      boxWidth:320,
      boxHeight:240,
      onChange: updatePreview,
      onSelect: updatePreview,
      allowResize:false,
      aspectRatio:1
      //aspectRatio: xsize / ysize
    },function(){
      // Use the API to get the real image size
      //var bounds = this.getBounds();
      var bounds = this.getBounds();
      boundx = bounds[0];
      boundy = bounds[1];
      //alert(boundx)
      //alert(boundy)
      // Store the API in the jcrop_api variable
      jcrop_api = this;
      //jcrop_api.setImage(imgsrc);
      // Move the preview into the jcrop container for css positioning
      $preview.appendTo(jcrop_api.ui.holder);
    });

    function updatePreview(c)
    {
      if (parseInt(c.w) > 0)
      {
        var rx = xsize / c.w;
        var ry = ysize / c.h;

        console.log('xsize',xsize);
        console.log('ysize',ysize);
        console.log('w',c.w);
        console.log('h',c.h);
        console.log('y',c.y);
        console.log('x',c.x);
        console.log('rx',rx);
        console.log('ry',ry);
        console.log('boundx',boundx);
        console.log('boundy',boundy);


        img_top_margin=c.y;
        img_left_margin=c.x;
        img_width=c.w;
        img_height=c.h;


        $pimg.css({
          width: Math.round(rx * boundx) + 'px',
          height: Math.round(ry * boundy) + 'px',
          marginLeft: '-' + Math.round(rx * c.x) + 'px',
          marginTop: '-' + Math.round(ry * c.y) + 'px'
        });

        console.log('width',Math.round(rx * boundx));
        console.log('height',Math.round(ry * boundy));
        console.log('marginLeft',Math.round(rx * c.x));
        console.log('marginTop',Math.round(ry * c.y));

      }
    };


       function replace_image() {
        console.log("==========replace_image=======");

        console.log("marginTop:"+img_top_margin);
        console.log("marginLeft:"+img_left_margin);

        console.log("width:"+img_width);
        console.log("height:"+img_height);
        img_file=$("#img_preview").attr("src")
        $.ajax({
            type: "POST",
            url: "/do_imgreplace/",
            data:{
             imgfile : img_file,
             marginTop : img_top_margin,
             marginLeft : img_left_margin,
             width : img_width,
             height: img_height
             },
            dataType: "json",
            success: function (json) {
                //alert(json.files);
                //add_question();
                alert('添加成功!');
            }
        })
    }
    function add_picture_result(data){
        $('#addform')[0].reset()
        $('#file-pic').fileinput('reset');
        $('#file-music').fileinput('reset');
        //alert(data)
        if (data.data == 'true') {
            replace_image();
            //alert('添加成功!');
        }
        else {
            alert(data);
        }
    }
    function add_question_result(data) {
        $('#addform')[0].reset()
        $('#file-pic').fileinput('reset');
        $('#file-music').fileinput('reset');
        //alert(data)
        if (data.data == 'true') {
            alert('添加成功!');
        }
        else {
            alert(data);
        }
    }
    function error_alert(){
        alert("error!");
    }

})








