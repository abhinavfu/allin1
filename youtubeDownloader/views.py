from django.shortcuts import render
from .models import *
# manually
import pytube
# Create your views here.

ylink = "youtube link"


def homeyd(request):
    # ---------------------------------------------------------
    #  home views count
    try:
        yt_count = Youtube_page_view_count.objects.get(id=1)
        yt_count.home_view_count += 1
        yt_count.save()
    except:
        pass
    # ---------------------------------------------------------
    yl = ""
    try:
        if request.method == "POST":
            global ylink
            ylink = request.POST["ylink"]
            con = pytube.YouTube(ylink)
            if ylink:
                # ---------------------------------------------------------
                #  home views count
                try:
                    yt_count = Youtube_page_view_count.objects.get(id=1)
                    yt_count.yt_download_view_count += 1
                    yt_count.save()
                except:
                    pass
                # ---------------------------------------------------------
                yl = "Link Found"
                title = con.title
                thumbnail = con.thumbnail_url
                format = con.streams

                res_form = []
                num = 0
                for i in format:
                    i = str(i)

                    def id(x):
                        return i.find(x)+len(x)
                    b = id('mime_type=')  # 10
                    c = id('res=')  # 4
                    d = id('fps=')  # 4
                    e = id('abr=')  # 4

                    if f'mime_type={i[b:b+7]}' == 'mime_type="audio/':
                        res_form.append(
                            {'id': num, 'abr': i[e:id('acodec')-7],
                             'format': i[b:e-5]})
                    else:
                        res_form.append(
                            {'id': num, 'resolution': i[c:d-5], 'format': i[b:c-5]})
                    num += 1
            else:
                yl = "Link not found"
            return render(request, 'homeyd.html', {'result': yl, 'title': title, 'thumbnail': thumbnail, "res_form": res_form})
    except:
        yl = "Link Problem"
    return render(request, 'homeyd.html', {'result': yl})


def ydownload(request, pk):
    con = pytube.YouTube(ylink)
    format = con.streams
    pos_quality = int(pk)  # number only
    try:
        # location = "Download location"
        try:
            location = r"C:\Users\aabhi\Downloads\Video"
            format[pos_quality].download(location)
        except:
            format[pos_quality].download()

        status = "Downloading Finished"
    except:
        status = "Downloading failed"
    return render(request, 'ydownload.html', {'status': status})
