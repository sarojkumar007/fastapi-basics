# import asyncio
# import uvicorn
# # import logging
#
# # logger = logging.getLogger(__name__)
#
# def shutdown_rest_of_app(_, __):
#     raise KeyboardInterrupt
#
# # @app.on_event("startup")
# # def startup_hook():
# #     import signal
#
# #     signal.signal(signal.SIGINT, shutdown_rest_of_app)
#
# def main():
#     try:
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)
#
#         web_config = uvicorn.Config(
#             "main:app",
#             host="127.0.0.1",
#             port=8000,
#             reload = True
#         )
#
#         web_server = uvicorn.Server(config=web_config)
#         loop.create_task(web_server.serve())
#         loop.run_forever()
#     except KeyboardInterrupt:
#         print("Caught Ctrl+C. Exiting gracefully.")
#     except Exception as e:
#         print("Exit")
#
# if __name__ == "__main__":
#     try:
#         main()
#     except KeyboardInterrupt:
#         print("Caught Ctrl+C")
#     except:
#         print('Exited')


# TYPE:2
import sys
import uvicorn
import os


if __name__ == '__main__':
    if not os.environ.get('VIRTUAL_ENV'):
        print("Enabling a Virtual Environment is recommended")
        exit()

    action = sys.argv[1] if len(sys.argv) > 1 else 'start'

    match action:
        case 'start':
            uvicorn.run('main:app', reload=True)
