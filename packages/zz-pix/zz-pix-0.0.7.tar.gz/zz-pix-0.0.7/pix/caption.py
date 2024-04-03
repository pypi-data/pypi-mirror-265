import logging
from typing import List, Union

import PIL
import torch
import tqdm
from termcolor import colored
from transformers import logging as hf_logging
from transformers import pipeline


# Convert a list of images to a dataset
# https://huggingface.co/docs/transformers/en/main_classes/pipelines#pipeline-batching
class ListDataset(torch.utils.data.Dataset):
    def __init__(self, original_list):
        self.original_list = original_list

    def __len__(self):
        return len(self.original_list)

    def __getitem__(self, i):
        return self.original_list[i]


class Blip:

    def __init__(self, large=False, cpu=False, blip2=False):
        self._configure_logging()
        self.model_type, model_name = self._select_model(large, blip2)
        self.use_cuda = self._determine_cuda_usage(cpu)
        self.captioner = self._create_captioner(model_name, self.use_cuda)

    def _configure_logging(self):
        # Suppress specific logging levels for a cleaner output
        logging.getLogger("transformers").setLevel(logging.ERROR)
        hf_logging.set_verbosity_error()

    def _select_model(self, large, blip2):
        # Select the appropriate model based on the parameters
        if blip2:
            model_type = "blip2"
            model_name = (
                "Salesforce/blip2-opt-2.7b" if not large else "Salesforce/blip2-opt-6.7b-coco"
            )
            print("Using Blip2 model")
        else:
            model_type = "blip"
            model_name = (
                "Salesforce/blip-image-captioning-base"
                if not large
                else "Salesforce/blip-image-captioning-large"
            )
        return model_type, model_name

    def _determine_cuda_usage(self, cpu):
        # Determine whether to use CUDA based on the user preference and availability
        if cpu or not torch.cuda.is_available():
            print(
                colored(
                    "Using CPU. This will be slow. To use GPU:\n"
                    "1. 'pip uninstall torch'\n2. Visit 'https://pytorch.org/' to install the appropriate version.\n",
                    "yellow",
                )
            )
            return False
        return True

    def _create_captioner(self, model_name, use_cuda):
        # Create the captioner pipeline with the selected model and device
        device = torch.device("cuda:0" if use_cuda else "cpu")
        return pipeline("image-to-text", model=model_name, device=device)

    def _batch_size_warning(self, batch_size, use_cuda):
        if batch_size > 2 and not use_cuda:
            print(
                colored(
                    "Batch size is greater than 2 and using CPU. This may cause memory issues. "
                    "Forcing batch size to 2. Consider using a GPU or reducing the batch size.",
                    "yellow",
                )
            )
            batch_size = 2
        elif batch_size > 8:
            print(
                colored(
                    "Batch size is greater than 8. This may cause memory issues. "
                    "Consider reducing the batch size.",
                    "yellow",
                )
            )

        return batch_size

    def caption_image(
        self,
        image_path: Union[str, List[str]],
        max_tokens=10,
        seed=None,
        temperature=1.0,
        batch_size=8,
        prompt=None,
    ) -> List[str]:
        try:
            if seed:
                torch.manual_seed(seed)

            batch_size = self._batch_size_warning(batch_size, self.use_cuda)

            # https://huggingface.co/docs/transformers/en/main_classes/text_generation
            kwargs = {
                "do_sample": True,
                "max_new_tokens": max_tokens,
                "temperature": temperature,
            }
            dataset = ListDataset(image_path)
            captions = []

            # tqdm is used to show a progress bar
            # https://huggingface.co/docs/transformers/en/main_classes/pipelines#pipeline-batching
            for out in tqdm.tqdm(
                self.captioner(
                    dataset, batch_size=batch_size, generate_kwargs=kwargs, prompt=prompt
                ),
                total=len(dataset),
            ):
                captions.append(out)

            return captions
        except PIL.UnidentifiedImageError as e:
            print(colored(f"Error Identifying Image: {e}", "red"))
            return None
