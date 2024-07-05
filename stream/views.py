from django.http import JsonResponse
from .utils import convert_rtsp_to_hls, get_output_dir, stop_stream

def start_stream(request):
    rtsp_url = request.GET.get('rtsp_url')
    if not rtsp_url:
        return JsonResponse({'error': 'RTSP URL is required'}, status=400)

    output_dir = get_output_dir(rtsp_url)
    convert_rtsp_to_hls(rtsp_url, output_dir)
    hls_url = f'/{output_dir}/index.m3u8'
    return JsonResponse({'hls_url': hls_url})

def stop_stream_view(request):
    hls_url = request.GET.get('hls_url')
    print("hlshls: ", hls_url)
    if not hls_url:
        return JsonResponse({'error': 'HLS URL is required'}, status=400)
    
    output_dir = hls_url.lstrip('/')
    stop_stream(output_dir)
    return JsonResponse({'message': 'Stream stopped and files deleted'})