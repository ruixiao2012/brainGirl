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
    uploadExtraData:{type:'picture'},
    previewFileType: "image",
	browseClass: "btn btn-success",
	browseLabel: "Pick Image",
	browseIcon: '<i class="glyphicon glyphicon-picture"></i>',
	removeClass: "btn btn-danger",
	removeLabel: "Delete",
	removeIcon: '<i class="glyphicon glyphicon-trash"></i>',
	uploadClass: "btn btn-info",
	uploadLabel: "Upload",
	uploadIcon: '<i class="glyphicon glyphicon-upload"></i>',
	showRemove: false,
	showUpload: false
    }).on("filebatchselected", function(event, files) {
    // trigger upload method immediately after files are selected
        $("#file-pic").fileinput("upload");
    });

    $('#file-pic').on('fileuploaded', function(event, data, previewId, index) {
    //var form = data.form, files = data.files, extra = data.extra,
    //    response = data.response, reader = data.reader;
    //alert(data.response.files);
    $('#attach_pic').val(data.response.files);


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
    });




     $('#file-music').on('fileuploaded', function(event, data, previewId, index) {
    //var form = data.form, files = data.files, extra = data.extra,
    //    response = data.response, reader = data.reader;
    //alert(data.response.files);
    length=$("#"+previewId).children("audio:eq(0)")[0].duration
    if(length<7)
    alert("歌曲不得小于7秒")
    if(length>13)
    alert("歌曲不得大于13秒")
    $('#file-music').fileinput('reset');
    return
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
            return false;
        }
        else {
            alert('请检查输入是否为空！')
        }


    });


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







