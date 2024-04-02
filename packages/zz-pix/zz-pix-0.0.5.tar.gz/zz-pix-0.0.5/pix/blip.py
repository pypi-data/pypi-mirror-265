import logging
from typing import List, Union

import PIL
import torch
from termcolor import colored
from transformers import logging as transformers_logging
from transformers import pipeline


class Blip:
    def __init__(self, large=False, cpu=False, blip2=False):
        logging.basicConfig(level=logging.ERROR)
        transformers_logging.set_verbosity_error()
        self.model_type = "blip"
        model_name = "Salesforce/blip-image-captioning-base"
        if large:
            model_name = "Salesforce/blip-image-captioning-large"
        if blip2:
            self.model_type = "blip2"
            print("Using Blip2 model")
            model_name = "Salesforce/blip2-opt-2.7b"
            if large:
                model_name = "Salesforce/blip2-opt-6.7b-coco"

        if cpu:
            print(colored("Using CPU. This will be slow.", "yellow"))
            use_cuda = False
        else:
            cuda_avaliable = torch.cuda.is_available()
            if not cuda_avaliable:
                print(
                    colored(
                        "CUDA is not available. Using CPU. Visit https://pytorch.org/ to install pytorch.",
                        "yellow",
                    )
                )
            use_cuda = cuda_avaliable
        self.captioner = pipeline(
            "image-to-text",
            model=model_name,
            device=torch.device("cuda:0" if use_cuda else "cpu"),
        )

    def caption_image(
        self,
        image_path: Union[str, List[str]],
        max_tokens=10,
        seed=None,
        temperature=1.0,
        batch_size=8,
        prompt=None,
        question=False,
    ) -> List[str]:
        try:
            if seed:
                torch.manual_seed(seed)

            # https://huggingface.co/docs/transformers/en/main_classes/text_generation
            kwargs = {
                "do_sample": True,
                "max_new_tokens": max_tokens,
                "temperature": temperature,
            }
            if self.model_type == "blip2":
                if question:
                    if not prompt:
                        prompt = "Question: What is this? Answer:"
                    else:
                        prompt = "Question: " + prompt + " Answer:"
                else:
                    prompt = prompt or "This is a photo of"
                captions = self.captioner(
                    image_path, batch_size=batch_size, generate_kwargs=kwargs, prompt=prompt
                )
            else:
                captions = self.captioner(image_path, batch_size=batch_size, generate_kwargs=kwargs)

            return captions
        except PIL.UnidentifiedImageError as e:
            print(f"Error: {e}")
            return None
