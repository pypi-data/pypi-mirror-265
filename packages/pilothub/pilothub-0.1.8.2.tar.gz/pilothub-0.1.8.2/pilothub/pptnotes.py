from pilothub.pptx2content import PPTxFile


class PPTx2Notes(PPTxFile):
    def __init__(self, file_path):
        super().__init__(file_path)
    
    def write_notes_to_pptx(self, output_path: str, 
                            content_client,
                            SET_SLIDE_TEXT_FOR_SKIP_SLIDES: bool = True,
                            SET_AI_TEXT_FOR_SKIP_SLIDES: bool = False,
                            AI_PROPMT_SKIP_SLIDES: str = None,
                            AI_PROMPT_DICT_SKIP_SLIDES: dict[str, str] = None,
                            DEFAULT_PROMPT_FOR_OTHER_SLIDES: str = None,
                            SKIP_NOTES_FOR_SLIDES_WITH_NOTES: bool = False,
                            ):
        """
        Write notes to the PPTx file.

        :param output_path: Path to save the PPTx file.
        :param content_client: Content client to use for generating notes.
        :param SET_SLIDE_TEXT_FOR_SKIP_SLIDES: Whether to set slide text for skip slides.
        :param SET_AI_TEXT_FOR_SKIP_SLIDES: Whether to set AI text for skip slides.
        :param AI_PROPMT_SKIP_SLIDES: Prompt to use for skip slides.
        :param AI_PROMPT_DICT_SKIP_SLIDES: Dictionary of prompts to use for skip slides.
        :param DEFAULT_PROMPT_FOR_OTHER_SLIDES: Prompt to use for other slides.
        :param SKIP_NOTES_FOR_SLIDES_WITH_NOTES: Whether to skip slides with existing notes.
        """
        self.content_client = content_client
        for i, slide in enumerate(self.slides):
            slide_text = self.get_slide_text(slide)
            layout = slide.slide_layout.name

            # check if slide has notes and need to skip the slide
            if SKIP_NOTES_FOR_SLIDES_WITH_NOTES:
                # check if text size of existing notes is greater than 10 letters
                if len(self.get_slide_notes(slide)) > 10:
                    continue
                else:
                    pass
            # check if skip slide
            if (i in self.skip_slides_index) or \
                (layout in self.skip_slides_layout):
                if SET_SLIDE_TEXT_FOR_SKIP_SLIDES:
                    if SET_AI_TEXT_FOR_SKIP_SLIDES:
                        if AI_PROMPT_DICT_SKIP_SLIDES is None:
                            if AI_PROPMT_SKIP_SLIDES is None:
                                raise ValueError("Please provide a prompt for AI.")
                            else:
                                prompt = AI_PROPMT_SKIP_SLIDES
                        else:
                            if layout not in AI_PROMPT_DICT_SKIP_SLIDES:
                                prompt = AI_PROPMT_SKIP_SLIDES
                            else:
                                prompt = AI_PROMPT_DICT_SKIP_SLIDES[layout]                    
                        notes_text = self.content_client.get_notes_from_text(
                            text=slide_text, prompt=prompt)
                        self.set_slide_notes(slide, notes_text)
                    else:
                        self.set_slide_notes(slide, slide_text)
                else:
                    self.erase_slide_notes(slide)
            elif slide.shapes.title and slide.shapes.title.text.lower().strip() in self.skip_slide_titles:
                self.set_slide_notes(slide, slide_text)
            else:
                prompt = DEFAULT_PROMPT_FOR_OTHER_SLIDES
                notes_text = self.content_client.get_notes_from_text(
                    text=slide_text, prompt=prompt)
                self.set_slide_notes(slide, notes_text)
        self.prs.save(output_path)