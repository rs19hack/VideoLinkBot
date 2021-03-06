import urlparse as up
import re

def get_host_code(url):
    code = None
    parsed = up.urlparse(url)
    for elem in parsed.netloc.split('.'):
        try:
            code = supported_domains[elem]
        except:
            continue
    return code


##############################################################

# compile regexs outside link cleaning functions to ensure it is only compiled
# once to make sure regexp compilation doesn't detract from performance
yt_video_id_pat = re.compile('v=([A-Za-z0-9_-]+)')

def youtube_link_cleaner(link):
    parsed = up.urlparse(link)
    short_link = None
    video_id = None
    if parsed.netloc == 'www.youtube.com' or parsed.netloc == 'm.youtube.com':
        match = re.search(yt_video_id_pat, link)
        if match:
            video_id = match.group()[2:]
    elif parsed.netloc == 'youtu.be':
        video_id = parsed.path[1:] # I feel like maybe I should split on '/' and then take item 0 instead        
    elif parsed.netloc == 'youtube.googleapis.com':
        try:
            video_id = parsed.path[3:]
        except:
            pass
    if video_id:
        short_link = 'http://youtu.be/' + video_id
    return short_link

def youtube_title_cleaner(title):
    return title[:-10]
    
#################################################################

def liveleak_link_cleaner(link):
    parsed = up.urlparse(link)
    clean = None
    if up.urlparse(link).path == '/view':
        clean = link
    return clean

def liveleak_title_cleaner(title):
    return title[15:]

#################################################################

vimeo_video_pat = re.compile('.*vimeo\.com/[0-9]+')

def vimeo_link_cleaner(link):
    clean = None
    video_url = re.findall(vimeo_video_pat, link)
    if video_url:
        clean =  video_url[0]
    return clean

def vimeo_title_cleaner(title):
    return title[:-9]

#################################################################

def ytd_title_cleaner(title):
    #if len(title) < 49
    #return title[:-49]
    return title.split(' by VJ')[0]

#################################################################

def nv_title_cleaner(title):
    return title[:-18]

#################################################################

def default_link(link):
    return link
    
def default_title(title):
    return title

link_cleaners     = {'yt':youtube_link_cleaner
                    ,'lk':liveleak_link_cleaner
                    ,'vm':vimeo_link_cleaner
                    ,'ytd':default_link
                    ,'nv':default_link
                    } 
title_cleaners = {'yt':youtube_title_cleaner
                 ,'lk':liveleak_title_cleaner
                 ,'vm':vimeo_title_cleaner
                 ,'ytd':ytd_title_cleaner
                 ,'nv':nv_title_cleaner
                 }

# netloc.split('.'):VLB_domain_code
supported_domains = {'youtube':'yt'
                    ,'youtu':'yt'
                    ,'liveleak':'lk'
                    ,'vimeo':'vm'
                    ,'youtubedoubler':'ytd'
                    ,'nicovideo':'nv'
                    }

